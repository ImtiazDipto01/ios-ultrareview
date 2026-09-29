#!/usr/bin/env python3
"""Create local snapshot fixtures; reviewer repositories never contain evaluator oracles.

No network, credentials, remote repositories, simulator, or device access is used.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess

PACKAGE = '''// swift-tools-version: 6.0
import PackageDescription
let package = Package(name: "ReviewFixture", platforms: [.iOS(.v17), .macOS(.v14)], products: [.library(name: "ReviewFixture", targets: ["ReviewFixture"])], targets: [.target(name: "ReviewFixture"), .testTarget(name: "ReviewFixtureTests", dependencies: ["ReviewFixture"])])
'''
SMOKE = '''import XCTest
@testable import ReviewFixture
final class SmokeTests: XCTestCase {
    func testModuleLoads() { XCTAssertTrue(true) }
}
'''
COMMON = '''# Review fixture

This repository is a complete local snapshot for the component and consumers described in PRODUCT.md. The Swift package validates the portable domain module. Apple-platform adapters are supplied in PlatformIntegration and are outside the portable package; there is no app scheme, signing identity, simulator session or hardware result in this fixture. No historical CI result is supplied. Platform behavior must be assessed honestly against these evidence limits.

The repository has no build plugins, external dependencies or network commands. Relevant source, adapters and configuration are all included. Tests are existing smoke coverage unless their names state otherwise.
'''
CASES = [
{
 'id':'scene_state', 'title':'Add document selection to two windows',
 'requirements':'''The editor supports two simultaneously active iPad windows. Selecting a document changes only that window's selection. Shared catalogue records remain shared. Each new scene begins without a selected document, and scene restoration applies only the activity belonging to that scene.\n''',
 'base': {
 'Sources/ReviewFixture/DocumentState.swift':'''import Foundation
import Observation
@MainActor public final class Catalogue {
    public let documentIDs = ["A", "B"]
    public init() {}
}
@MainActor @Observable public final class Selection {
    public var documentID: String?
    public init() {}
}
@MainActor public final class WindowModel {
    public let catalogue: Catalogue
    public let selection: Selection
    public init(catalogue: Catalogue, selection: Selection) {
        self.catalogue = catalogue
        self.selection = selection
    }
    public func select(_ id: String) { selection.documentID = id }
    public func restore(documentID: String?) { selection.documentID = documentID }
}
@MainActor public final class AppServices {
    public let catalogue = Catalogue()
    public init() {}
    public func makeWindow() -> WindowModel { WindowModel(catalogue: catalogue, selection: Selection()) }
}
''',
 'PlatformIntegration/EditorScene.swift':'''import SwiftUI
import ReviewFixture
@main struct EditorApp: App {
    @State private var services = AppServices()
    var body: some Scene { WindowGroup { EditorScene(services: services) } }
}
struct EditorScene: View {
    @State private var model: WindowModel
    init(services: AppServices) { _model = State(initialValue: services.makeWindow()) }
    var body: some View {
        VStack {
            Text(model.selection.documentID ?? "No selection")
            Button("Open A") { model.select("A") }
        }
    }
}
'''
 },
 'clean': {'Sources/ReviewFixture/DocumentState.swift': None},
 'defect': {'Sources/ReviewFixture/DocumentState.swift': None},
 'oracle': {'severity':'P1','path':'Sources/ReviewFixture/DocumentState.swift','needle':'selection: selection','trace':'Two scenes receive the same mutable Selection; select or restore in the second scene changes the first window selection. Catalogue sharing is intentional, selection sharing violates independent windows.'}
},
{
 'id':'background_recovery','title':'Schedule catalogue updates between launches',
 'requirements':'''The catalogue may be stale after hours without a background refresh. Entering the foreground must refresh the visible catalogue independently of whether a refresh request was previously submitted. Refresh scheduling is a best-effort optimization; a submitted request is not proof of delivery. Failed refresh keeps the previous catalogue and allows a later foreground attempt.\n''',
 'base': {
 'Sources/ReviewFixture/CatalogueRefresh.swift':'''public protocol RefreshScheduling: Sendable { func submit() async throws }
public protocol CatalogueFetching: Sendable { func fetch() async throws -> [String] }
@MainActor public final class RefreshCoordinator {
    private let scheduler: any RefreshScheduling
    private let service: any CatalogueFetching
    public private(set) var items: [String] = []
    public private(set) var errorMessage: String?
    public init(scheduler: any RefreshScheduling, service: any CatalogueFetching) {
        self.scheduler = scheduler
        self.service = service
    }
    public func scheduleNextRefresh() async { try? await scheduler.submit() }
    public func enteredForeground() async { await refresh() }
    public func backgroundTaskDelivered() async { await refresh() }
    private func refresh() async {
        do { items = try await service.fetch(); errorMessage = nil }
        catch { errorMessage = "Refresh unavailable" }
    }
}
''',
 'PlatformIntegration/RefreshDelivery.swift':'''import BackgroundTasks
import UIKit
import ReviewFixture
struct SystemScheduler: RefreshScheduling {
    func submit() async throws {
        let request = BGAppRefreshTaskRequest(identifier: "fixture.catalogue.refresh")
        request.earliestBeginDate = Date(timeIntervalSinceNow: 900)
        try BGTaskScheduler.shared.submit(request)
    }
}
@MainActor final class SceneDelivery {
    let refresh: RefreshCoordinator
    init(refresh: RefreshCoordinator) { self.refresh = refresh }
    func sceneDidBecomeActive() { Task { await refresh.enteredForeground() } }
    func sceneDidEnterBackground() { Task { await refresh.scheduleNextRefresh() } }
}
''',
 'PlatformIntegration/Info.plist':'''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>BGTaskSchedulerPermittedIdentifiers</key><array><string>fixture.catalogue.refresh</string></array><key>UIBackgroundModes</key><array><string>fetch</string></array></dict></plist>'''
 },
 'clean':{'Sources/ReviewFixture/CatalogueRefresh.swift':None},
 'defect':{'Sources/ReviewFixture/CatalogueRefresh.swift':None},
 'oracle': {'severity':'P1','path':'Sources/ReviewFixture/CatalogueRefresh.swift','needle':'if !refreshRequested','trace':'A successful submit sets refreshRequested permanently even if the system never delivers the task; foreground skips fetching thereafter, so core catalogue stops updating. Submission cannot guarantee delivery.'}
},
{
 'id':'watch_delivery','title':'Send completed watch workout summaries to the phone',
 'requirements':'''A completed watch workout summary is saved durably on the watch before delivery. It must reach the phone when connectivity later permits, even when the phone app is inactive or unreachable at workout completion. The phone import is idempotent by workout ID. Delete the pending watch record only after the phone confirms durable import. Immediate reachability is not guaranteed. This PR changes only dispatch choice; existing acknowledgement handling and persistence stay in place.\n''',
 'base':{
 'Sources/ReviewFixture/WorkoutDelivery.swift':'''import Foundation
public struct Workout: Codable, Sendable { public let id: String; public let seconds: Int; public init(id: String, seconds: Int) { self.id = id; self.seconds = seconds } }
public protocol SummaryTransport: Sendable {
    func enqueue(_ payload: Data) async
    func sendInteractive(_ payload: Data) async throws
}
public protocol PendingWorkouts: Sendable {
    func save(_ workout: Workout) async throws
    func all() async throws -> [Workout]
    func remove(id: String) async throws
}
public actor WorkoutDelivery {
    private let transport: any SummaryTransport
    private let pending: any PendingWorkouts
    public init(transport: any SummaryTransport, pending: any PendingWorkouts) { self.transport = transport; self.pending = pending }
    public func completed(_ workout: Workout) async throws {
        try await pending.save(workout)
        await flush()
    }
    public func flush() async {
        guard let workouts = try? await pending.all() else { return }
        for workout in workouts {
            guard let payload = try? JSONEncoder().encode(workout) else { continue }
            await transport.enqueue(payload)
        }
    }
    public func importedAcknowledgement(id: String) async throws { try await pending.remove(id: id) }
}
''',
 'PlatformIntegration/WatchTransport.swift':'''import WatchConnectivity
import Foundation
import ReviewFixture
actor SessionReadiness {
    private var activated = false
    private var waiters: [CheckedContinuation<Void, Never>] = []
    func waitUntilActivated() async {
        if activated { return }
        await withCheckedContinuation { waiters.append($0) }
    }
    func didActivate() {
        activated = true
        for waiter in waiters { waiter.resume() }
        waiters.removeAll()
    }
}
final class WatchTransport: NSObject, SummaryTransport, WCSessionDelegate, @unchecked Sendable {
    private let session = WCSession.default
    private let readiness = SessionReadiness()
    weak var delivery: WorkoutDelivery?
    override init() { super.init(); session.delegate = self; session.activate() }
    func enqueue(_ payload: Data) async {
        await readiness.waitUntilActivated()
        session.transferUserInfo(["workout": payload])
    }
    func sendInteractive(_ payload: Data) async throws {
        await readiness.waitUntilActivated()
        try await withCheckedThrowingContinuation { (continuation: CheckedContinuation<Void, Error>) in
            session.sendMessage(["workout": payload], replyHandler: { _ in continuation.resume() }, errorHandler: { continuation.resume(throwing: $0) })
        }
    }
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        guard activationState == .activated else { return }
        Task { await readiness.didActivate(); await delivery?.flush() }
    }
    func session(_ session: WCSession, didReceiveUserInfo userInfo: [String: Any] = [:]) {
        guard let id = userInfo["importedWorkoutID"] as? String else { return }
        Task { try? await delivery?.importedAcknowledgement(id: id) }
    }
    #if os(iOS)
    func sessionDidBecomeInactive(_ session: WCSession) {}
    func sessionDidDeactivate(_ session: WCSession) { session.activate() }
    #endif
}
''',
 'PlatformIntegration/WorkoutConsumers.swift':'''import Foundation
import WatchConnectivity
import ReviewFixture
actor FilePending: PendingWorkouts {
    let directory: URL
    init(directory: URL) throws {
        self.directory = directory
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    func save(_ workout: Workout) async throws {
        let url = directory.appendingPathComponent(workout.id).appendingPathExtension("json")
        try JSONEncoder().encode(workout).write(to: url, options: .atomic)
    }
    func all() async throws -> [Workout] {
        try FileManager.default.contentsOfDirectory(at: directory, includingPropertiesForKeys: nil)
            .filter { $0.pathExtension == "json" }
            .map { try JSONDecoder().decode(Workout.self, from: Data(contentsOf: $0)) }
    }
    func remove(id: String) async throws {
        let url = directory.appendingPathComponent(id).appendingPathExtension("json")
        if FileManager.default.fileExists(atPath: url.path) { try FileManager.default.removeItem(at: url) }
    }
}
@MainActor final class WatchComposition {
    let transport: WatchTransport
    let delivery: WorkoutDelivery
    init(pendingDirectory: URL) throws {
        transport = WatchTransport()
        delivery = WorkoutDelivery(transport: transport, pending: try FilePending(directory: pendingDirectory))
        transport.delivery = delivery
    }
    func completedWorkout(id: UUID, seconds: Int) async throws {
        try await delivery.completed(Workout(id: id.uuidString, seconds: seconds))
    }
    func appActivated() { Task { await delivery.flush() } }
}
actor PhoneImporter {
    let directory: URL
    init(directory: URL) throws {
        self.directory = directory
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    func importOnce(_ workout: Workout) throws {
        let url = directory.appendingPathComponent(workout.id).appendingPathExtension("json")
        if !FileManager.default.fileExists(atPath: url.path) { try JSONEncoder().encode(workout).write(to: url, options: .atomic) }
    }
}
final class PhoneSession: NSObject, WCSessionDelegate, @unchecked Sendable {
    let importer: PhoneImporter
    private let session = WCSession.default
    init(importer: PhoneImporter) { self.importer = importer; super.init(); session.delegate = self; session.activate() }
    func session(_ session: WCSession, didReceiveUserInfo userInfo: [String: Any] = [:]) {
        guard let data = userInfo["workout"] as? Data else { return }
        Task {
            guard let workout = try? JSONDecoder().decode(Workout.self, from: data), (try? await importer.importOnce(workout)) != nil else { return }
            session.transferUserInfo(["importedWorkoutID": workout.id])
        }
    }
    func session(_ session: WCSession, didReceiveMessage message: [String: Any], replyHandler: @escaping ([String: Any]) -> Void) {
        guard let data = message["workout"] as? Data else { replyHandler([:]); return }
        Task {
            guard let workout = try? JSONDecoder().decode(Workout.self, from: data), (try? await importer.importOnce(workout)) != nil else { replyHandler([:]); return }
            session.transferUserInfo(["importedWorkoutID": workout.id])
            replyHandler(["importedWorkoutID": workout.id])
        }
    }
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {}
    #if os(iOS)
    func sessionDidBecomeInactive(_ session: WCSession) {}
    func sessionDidDeactivate(_ session: WCSession) { session.activate() }
    #endif
}
'''

 },
 'clean':{'Sources/ReviewFixture/WorkoutDelivery.swift':None},
 'defect':{'Sources/ReviewFixture/WorkoutDelivery.swift':None},
 'oracle': {'severity':'P1','path':'Sources/ReviewFixture/WorkoutDelivery.swift','needle':'try? await transport.sendInteractive','trace':'Interactive sendMessage requires reachability and does not enqueue durable background delivery. Completing while the phone is inactive and keeping the watch app closed leaves the phone without the promised summary until another watch activation. Existing transferUserInfo dispatch would queue without watch foreground activity.'}
},
{
 'id':'keychain_background','title':'Retain the account refresh credential across background renewals',
 'requirements':'''The app renews the account session during background processing after the device has been unlocked once since reboot, including while the screen is subsequently locked. Tokens must never migrate to another device, sync to iCloud or enter logs. Before first unlock, defer renewal rather than signing out. The app does not claim access before first unlock. This PR changes the storage accessibility for newly added refresh-token items.\n''',
 'base':{
 'Sources/ReviewFixture/CredentialPolicy.swift':'''public enum CredentialAccessibility: String, Sendable { case afterFirstUnlockDeviceOnly, whenUnlockedDeviceOnly }
public struct CredentialPolicy: Sendable {
    public var accessibility: CredentialAccessibility { .afterFirstUnlockDeviceOnly }
    public let synchronizable = false
    public init() {}
}
''',
 'PlatformIntegration/RefreshTokenStore.swift':'''import Security
import Foundation
import ReviewFixture
final class RefreshTokenStore {
    func insert(_ token: Data, account: String) throws {
        let policy = CredentialPolicy()
        let accessibility = policy.accessibility == .afterFirstUnlockDeviceOnly ? kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly : kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword, kSecAttrService as String: "fixture.account.refresh", kSecAttrAccount as String: account, kSecAttrAccessible as String: accessibility, kSecAttrSynchronizable as String: policy.synchronizable, kSecValueData as String: token]
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else { throw NSError(domain: NSOSStatusErrorDomain, code: Int(status)) }
    }
    func read(account: String) throws -> Data {
        let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword, kSecAttrService as String: "fixture.account.refresh", kSecAttrAccount as String: account, kSecReturnData as String: true]
        var result: CFTypeRef?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess, let data = result as? Data else { throw NSError(domain: NSOSStatusErrorDomain, code: Int(status)) }
        return data
    }
}
''',
 'PlatformIntegration/BackgroundRenewal.swift':'''import Foundation
import Security
protocol RenewalAPI { func renew(token: Data) async throws }
@MainActor final class BackgroundRenewal {
    let store = RefreshTokenStore()
    func run(account: String, api: any RenewalAPI) async -> Bool {
        do { try await api.renew(token: store.read(account: account)); return true }
        catch let error as NSError where error.code == Int(errSecInteractionNotAllowed) { return false }
        catch { return false }
    }
}
'''
 },
 'clean':{'Sources/ReviewFixture/CredentialPolicy.swift':None},
 'defect':{'Sources/ReviewFixture/CredentialPolicy.swift':None},
 'oracle': {'severity':'P1','path':'Sources/ReviewFixture/CredentialPolicy.swift','needle':'.whenUnlockedDeviceOnly','trace':'The inserted token becomes unavailable whenever the device is locked, including after first unlock. BackgroundRenewal then fails with errSecInteractionNotAllowed for a promised locked-screen renewal; the security requirement permits AfterFirstUnlockThisDeviceOnly.'}
},
{
 'id':'api_rollout','title':'Adopt the account display-name field in the profile feature',
 'requirements':'''The profile feature is independently shipped from the account backend. During staged rollout the client must accept both legacy responses containing name and new responses containing display_name. The disk cache contains the same DTO JSON from previous app versions and must remain readable. New encoding should use display_name; all supported cached old responses should still render the existing account name. The shared DTO and provider interface live in the ReviewFixture library; ProfileFeature consumes only this interface.\n''',
 'base':{
 'Sources/ReviewFixture/ProfileDTO.swift':'''import Foundation
public struct ProfileDTO: Codable, Sendable {
    public let id: String
    public let displayName: String
    public init(id: String, displayName: String) { self.id = id; self.displayName = displayName }
    enum CodingKeys: String, CodingKey { case id; case displayName = "name" }
}
public protocol ProfileProviding: Sendable { func profile() async throws -> ProfileDTO }
public struct ProfilePresentation: Sendable {
    public let title: String
    public init(profile: ProfileDTO) { title = profile.displayName }
}
''',
 'PlatformIntegration/ProfileFeature.swift':'''import Foundation
import ReviewFixture
struct CachedProfileProvider: ProfileProviding {
    let cacheURL: URL
    func profile() async throws -> ProfileDTO { try JSONDecoder().decode(ProfileDTO.self, from: Data(contentsOf: cacheURL)) }
}
func profileScreenTitle(provider: any ProfileProviding) async throws -> String {
    ProfilePresentation(profile: try await provider.profile()).title
}
''',
 'PlatformIntegration/Rollout.json':'{"backend": {"old_response": {"id": "7", "name": "Mina"}, "new_response": {"id": "7", "display_name": "Mina"}}, "stored_cache": {"id": "7", "name": "Mina"}}\n'
 },
 'clean':{'Sources/ReviewFixture/ProfileDTO.swift':None},
 'defect':{'Sources/ReviewFixture/ProfileDTO.swift':None},
 'oracle': {'severity':'P1','path':'Sources/ReviewFixture/ProfileDTO.swift','needle':'case displayName = "display_name"','trace':'Synthesized Codable decoding now requires display_name, so both still-served legacy backend responses and existing name-key cache fail with keyNotFound; core profile load fails during required mixed rollout.'}
},
{
 'id':'bounded_rename','title':'Clarify the profile badge normalizer private symbol',
 'requirements':'''Rename the internal normalizeLabel helper to trimmedLabel. Public API, normalization behavior and output must remain unchanged. The library has no device-specific imports or lifecycle work; it is used by an iOS profile feature and a macOS command-line importer. All behavior in this component is portable string normalization. Existing tests cover the public outcome, including whitespace-only labels.\n''',
 'base':{
 'Sources/ReviewFixture/BadgeLabel.swift':'''public struct BadgeLabel: Equatable, Sendable {
    public let text: String
    public init(raw: String) { text = Self.normalizeLabel(raw) }
    private static func normalizeLabel(_ raw: String) -> String {
        let trimmed = raw.trimmingCharacters(in: .whitespacesAndNewlines)
        return trimmed.isEmpty ? "Member" : trimmed
    }
}
import Foundation
public struct ProfileBadge: Sendable {
    public let label: BadgeLabel
    public init(accountLabel: String) { label = BadgeLabel(raw: accountLabel) }
}
''',
 'Tests/ReviewFixtureTests/SmokeTests.swift':'''import XCTest
@testable import ReviewFixture
final class BadgeLabelTests: XCTestCase {
    func testPublicProfileBadgePreservesNonemptyName() { XCTAssertEqual(ProfileBadge(accountLabel: "  Mina \\n").label.text, "Mina") }
    func testWhitespaceFallsBackToMember() { XCTAssertEqual(ProfileBadge(accountLabel: " \\n\\t ").label.text, "Member") }
    func testUnicodeAndInteriorSpacesPreserved() { XCTAssertEqual(BadgeLabel(raw: "  Renée Q. ").text, "Renée Q.") }
}
'''
 },
 'clean':{'Sources/ReviewFixture/BadgeLabel.swift':None},
 'oracle': {'findings':0,'expected_score':5.0,'trace':'Only a private symbol and its direct call site are renamed. Passing exact-head build/tests provide focused evidence for unchanged public behavior; no platform-specific gate is implicated.'}
}
]

def populate_variants():
    c=CASES[0]; base=c['base']['Sources/ReviewFixture/DocumentState.swift']; c['clean']['Sources/ReviewFixture/DocumentState.swift']=base.replace('public var documentID: String?', 'public private(set) var documentID: String?\n    public func select(_ id: String?) { documentID = id }').replace('selection.documentID = id', 'selection.select(id)').replace('selection.documentID = documentID', 'selection.select(documentID)')
    c['defect']['Sources/ReviewFixture/DocumentState.swift']=c['clean']['Sources/ReviewFixture/DocumentState.swift'].replace('public let catalogue = Catalogue()', 'public let catalogue = Catalogue()\n    private let selection = Selection()').replace('selection: Selection())', 'selection: selection)')
    c=CASES[1]; base=c['base']['Sources/ReviewFixture/CatalogueRefresh.swift']; c['clean']['Sources/ReviewFixture/CatalogueRefresh.swift']=base.replace('public private(set) var items', 'private var refreshRequested = false\n    public private(set) var items').replace('try? await scheduler.submit()', 'do { try await scheduler.submit(); refreshRequested = true }\n        catch { refreshRequested = false }'); c['defect']['Sources/ReviewFixture/CatalogueRefresh.swift']=c['clean']['Sources/ReviewFixture/CatalogueRefresh.swift'].replace('public func enteredForeground() async { await refresh() }', 'public func enteredForeground() async { if !refreshRequested { await refresh() } }')
    c=CASES[2]; base=c['base']['Sources/ReviewFixture/WorkoutDelivery.swift']; c['clean']['Sources/ReviewFixture/WorkoutDelivery.swift']=base.replace('guard let payload = try? JSONEncoder().encode(workout) else { continue }', 'let encoder = JSONEncoder()\n            guard let payload = try? encoder.encode(workout) else { continue }'); c['defect']['Sources/ReviewFixture/WorkoutDelivery.swift']=c['clean']['Sources/ReviewFixture/WorkoutDelivery.swift'].replace('await transport.enqueue(payload)', 'try? await transport.sendInteractive(payload)')
    c=CASES[3]; base=c['base']['Sources/ReviewFixture/CredentialPolicy.swift']; c['clean']['Sources/ReviewFixture/CredentialPolicy.swift']=base.replace('public var accessibility: CredentialAccessibility { .afterFirstUnlockDeviceOnly }', 'public let accessibility: CredentialAccessibility = .afterFirstUnlockDeviceOnly'); c['defect']['Sources/ReviewFixture/CredentialPolicy.swift']=c['clean']['Sources/ReviewFixture/CredentialPolicy.swift'].replace('= .afterFirstUnlockDeviceOnly', '= .whenUnlockedDeviceOnly')
    c=CASES[4]; base=c['base']['Sources/ReviewFixture/ProfileDTO.swift']; bad=base.replace('case displayName = "name"', 'case displayName = "display_name"'); c['defect']['Sources/ReviewFixture/ProfileDTO.swift']=bad; c['clean']['Sources/ReviewFixture/ProfileDTO.swift']=bad.replace('enum CodingKeys: String, CodingKey { case id; case displayName = "display_name" }', '''enum CodingKeys: String, CodingKey { case id; case displayName = "display_name"; case legacyName = "name" }
    public init(from decoder: any Decoder) throws {
        let values = try decoder.container(keyedBy: CodingKeys.self)
        id = try values.decode(String.self, forKey: .id)
        displayName = try values.decodeIfPresent(String.self, forKey: .displayName) ?? values.decode(String.self, forKey: .legacyName)
    }
    public func encode(to encoder: any Encoder) throws {
        var values = encoder.container(keyedBy: CodingKeys.self)
        try values.encode(id, forKey: .id)
        try values.encode(displayName, forKey: .displayName)
    }''')
    c=CASES[5]; c['clean']['Sources/ReviewFixture/BadgeLabel.swift']=c['base']['Sources/ReviewFixture/BadgeLabel.swift'].replace('normalizeLabel', 'trimmedLabel')

    domain_tests = [
        """import XCTest
@testable import ReviewFixture
final class WindowSelectionTests: XCTestCase {
    @MainActor func testTwoWindowsKeepSelectionsIndependent() async {
        let services = AppServices()
        let first = services.makeWindow()
        let second = services.makeWindow()
        first.select("A")
        second.restore(documentID: "B")
        XCTAssertEqual(first.selection.documentID, "A")
        XCTAssertEqual(second.selection.documentID, "B")
        XCTAssertTrue(first.catalogue === second.catalogue)
    }
}
""",
        """import XCTest
@testable import ReviewFixture
actor TestScheduler: RefreshScheduling { func submit() async throws {} }
actor TestCatalogueAPI: CatalogueFetching {
    var calls = 0
    func fetch() async throws -> [String] { calls += 1; return ["updated"] }
}
final class CatalogueRecoveryTests: XCTestCase {
    @MainActor func testForegroundRecoversWithoutBackgroundDelivery() async {
        let api = TestCatalogueAPI()
        let model = RefreshCoordinator(scheduler: TestScheduler(), service: api)
        await model.scheduleNextRefresh()
        await model.enteredForeground()
        XCTAssertEqual(model.items, ["updated"])
        let count = await api.calls
        XCTAssertEqual(count, 1)
    }
}
""",
        """import XCTest
@testable import ReviewFixture
actor TestTransport: SummaryTransport {
    var queued = 0
    var interactive = 0
    func enqueue(_ payload: Data) async { queued += 1 }
    func sendInteractive(_ payload: Data) async throws { interactive += 1; throw Unreachable() }
    struct Unreachable: Error {}
}
actor TestPending: PendingWorkouts {
    var records: [String: Workout] = [:]
    func save(_ workout: Workout) async throws { records[workout.id] = workout }
    func all() async throws -> [Workout] { Array(records.values) }
    func remove(id: String) async throws { records.removeValue(forKey: id) }
}
final class WorkoutDeliveryTests: XCTestCase {
    func testCompletedWorkoutQueuesWhilePhoneUnreachableAndKeepsPendingUntilAck() async throws {
        let transport = TestTransport()
        let pending = TestPending()
        let delivery = WorkoutDelivery(transport: transport, pending: pending)
        try await delivery.completed(Workout(id: "workout-1", seconds: 30))
        let queued = await transport.queued
        let interactive = await transport.interactive
        let retained = try await pending.all()
        XCTAssertEqual(queued, 1)
        XCTAssertEqual(interactive, 0)
        XCTAssertEqual(retained.count, 1)
        try await delivery.importedAcknowledgement(id: "workout-1")
        let remaining = try await pending.all()
        XCTAssertEqual(remaining.count, 0)
    }
}
""",
        """import XCTest
@testable import ReviewFixture
final class CredentialPolicyTests: XCTestCase {
    func testAllowsRenewalAfterFirstUnlockWhileRemainingDeviceBound() {
        let policy = CredentialPolicy()
        XCTAssertEqual(policy.accessibility, .afterFirstUnlockDeviceOnly)
        XCTAssertFalse(policy.synchronizable)
    }
}
""",
        """import XCTest
@testable import ReviewFixture
final class ProfileCompatibilityTests: XCTestCase {
    func testExistingCachedProfileRemainsReadable() throws {
        let old = Data(#"{"id":"7","name":"Mina"}"#.utf8)
        let profile = try JSONDecoder().decode(ProfileDTO.self, from: old)
        XCTAssertEqual(ProfilePresentation(profile: profile).title, "Mina")
    }
    func testNewServerProfileAndEncodingUseDisplayName() throws {
        let new = Data(#"{"id":"7","display_name":"Mina"}"#.utf8)
        let profile = try JSONDecoder().decode(ProfileDTO.self, from: new)
        let encoded = try JSONSerialization.jsonObject(with: JSONEncoder().encode(profile)) as! [String: String]
        XCTAssertEqual(encoded["display_name"], "Mina")
        XCTAssertNil(encoded["name"])
    }
}
"""
    ]
    for case, tests in zip(CASES[:5], domain_tests):
        case['clean']['Tests/ReviewFixtureTests/SmokeTests.swift'] = tests
        case['defect']['Tests/ReviewFixtureTests/SmokeTests.swift'] = tests

EVIDENCE_SCOPE = {'scene_state': 'Focused host tests prove selection ownership and catalogue sharing. Apple scene/window construction and SwiftUI rendering are not executed. Require app/runtime proof only for material changed obligations that these checks cannot exercise; a pure ownership refactor may use equivalent focused proof.', 'background_recovery': 'The host test executes successful scheduling followed by foreground recovery with no background delivery, proving the portable retry choice. It does not demonstrate BGTaskScheduler system delivery. The unchanged best-effort scheduler need not acquire a device-delivery gate merely because it exists.', 'watch_delivery': 'The host test proves enqueue-versus-interactive choice, durable-store retention and acknowledgement removal through fakes. It does not prove paired-device WCSession delivery or system suspension. Require device evidence for changed obligations depending on real pairing/system delivery, not merely for deterministic dispatch selection in unchanged adapters.', 'keychain_background': 'The host test proves the selected accessibility enum and disabled synchronization. Static adapter inspection establishes mapping to the named Security constant; it does not execute Keychain reads while locked. Require lock-state evidence when a changed obligation depends on actual protected-data availability, not for an unchanged constant refactor alone.', 'api_rollout': 'Focused host tests exercise legacy/new decoding, legacy cache representation, new encoding and the public presentation consumer. This contract is portable; unrelated device, network, backend deployment or app-scheme proof is not universal when these checks cover the scoped obligation.', 'bounded_rename': 'The exact-head portable build and three focused tests cover all changed scope. No Apple adapters, lifecycle, concurrency or device behavior are present.'}

def run(repo, *args):
    return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-C',str(repo),*args],text=True,env={**os.environ,'GIT_CONFIG_GLOBAL':os.devnull,'GIT_CONFIG_NOSYSTEM':'1','GIT_AUTHOR_NAME':'Fixture Builder','GIT_AUTHOR_EMAIL':'fixture@example.invalid','GIT_COMMITTER_NAME':'Fixture Builder','GIT_COMMITTER_EMAIL':'fixture@example.invalid'}).strip()

def write_files(repo, files):
    for name, content in files.items():
        assert content is not None
        path=repo/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('destination',type=Path); args=parser.parse_args()
    root=args.destination.resolve()
    if root.exists() and any(root.iterdir()): raise SystemExit(f'Refusing a non-empty destination: {root}')
    root.mkdir(parents=True,exist_ok=True)
    populate_variants(); oracle=[]; manifest=[]
    for index,case in enumerate(CASES,1):
        repo=root/f'{index:02d}-{case["id"]}'
        if repo.exists(): raise SystemExit(f'Refusing to overwrite existing fixture: {repo}')
        repo.mkdir()
        run(repo,'init','--quiet','--template=','-b','base'); run(repo,'config','user.name','Fixture Builder'); run(repo,'config','user.email','fixture@example.invalid')
        write_files(repo, {'Package.swift':PACKAGE, '.gitignore':'.build/\n', 'README.md':COMMON,'PRODUCT.md':'# '+case['title']+'\n\n'+case['requirements'],'Tests/ReviewFixtureTests/SmokeTests.swift':SMOKE,**case['base']})
        run(repo,'add','.'); run(repo,'commit','--quiet','-m','Establish component and existing consumers'); base=run(repo,'rev-parse','HEAD')
        row={'id':case['id'],'repository':str(repo),'base':base,'variants':{}}
        for variant_index, variant in enumerate(['clean','defect'], 1):
            if variant not in case: continue
            run(repo,'switch','--quiet','-c',f'snapshot-{variant_index}',base)
            write_files(repo,case[variant]); run(repo,'add','.'); run(repo,'commit','--quiet','-m',case['title']); sha=run(repo,'rev-parse','HEAD')
            row['variants'][variant]=sha
        # A clean dedicated fixture checkout. Reviewers should isolate independently.
        run(repo,'switch','--quiet','--detach',row['variants']['clean'])
        manifest.append(row); oracle.append({'id':case['id'],'oracle':case['oracle'],'clean_expected': {'score_if_only_supplied_evidence':4.0 if 'defect' in case else 5.0,'higher_score_condition':'Reviewer-executed checks may raise confidence when genuinely relevant to the scoped target; untouched adapters alone do not impose universal hardware gates. Apply actual skill caps and applicable evidence gates.' if 'defect' in case else 'Award 5.0 after the included focused host checks succeed on the exact target.','decision_if_only_supplied_evidence':'COMMENT' if 'defect' in case else 'APPROVE','findings':0,'limits':'A missing material baseline proof yields validation-limited 4.0/COMMENT; root must adjudicate reviewer-executed tests against the actual changed obligations. Do not infer a platform-wide app/device requirement.','evidence_scope_adjudication':EVIDENCE_SCOPE[case['id']]},'defect_expected':{'maximum_score':3.0 if case['oracle'].get('severity')=='P1' else 4.0,'decision':'REQUEST_CHANGES','root_causes':1} if 'defect' in case else None})
    (root/'evaluator').mkdir(); (root/'evaluator'/'oracle.json').write_text(json.dumps(oracle,indent=2)+'\n')
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    inputs=root/'inputs'; inputs.mkdir()
    sequence=[(0,'defect'),(0,'clean'),(1,'clean'),(1,'defect'),(2,'defect'),(2,'clean'),(3,'clean'),(3,'defect'),(4,'defect'),(4,'clean'),(5,'clean')]
    lookup=[]
    for number,(index,variant) in enumerate(sequence,1):
        row=manifest[index]
        prompt=inputs/f'input-{number:02d}.md'
        prompt.write_text(f"""Review this local snapshot with the assigned iOS UltraReview skill and produce its normal complete draft output. This is snapshot review; no provider comments or external writes are requested.

Repository: `{row['repository']}`
Base: `{row['base']}`
Head: `{row['variants'][variant]}`
Stated product intent: `PRODUCT.md` on that target.

Acquire the complete behavior-relevant diff and surrounding consumers from this repository. This is a normal checkout; preserve it and isolate the exact head as the skill requires. Locally authored dependency-free package builds/tests may run after inspecting their files. There is no app-scheme build, simulator or hardware evidence for Apple adapters. Do not claim any such run. The focused package tests exercise portable logic; they do not execute PlatformIntegration.

Treat only this repository and the named input as review input. Do not read sibling repositories, manifest.json, evaluator resources, the fixture builder, or evaluation expectations. The supplied component's entire impact radius is present; avoid inventing omitted production systems.

Report supported P0–P2 introduced or made relevant by the change, the honest evidence limits, merge-confidence score and finite threshold path. Do not post externally.
""")
        lookup.append({'input':str(prompt),'id':row['id'],'variant':variant,'base':row['base'],'head':row['variants'][variant]})
    (root/'evaluator'/'input-map.json').write_text(json.dumps(lookup,indent=2)+'\n')
    print(json.dumps({'root':str(root),'repositories':len(manifest),'snapshot_targets':sum(len(r['variants']) for r in manifest)},indent=2))
if __name__=='__main__': main()
