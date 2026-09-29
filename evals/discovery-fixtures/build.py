#!/usr/bin/env python3
"""Build green-visible-suite discovery controls; hide outcome tests outside repositories."""
import argparse
import copy
import importlib.util
import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fixturelib import commit,fresh,git,init,prompt,save,write
spec=importlib.util.spec_from_file_location('aided',Path(__file__).resolve().parents[1]/'expertise-fixtures/build.py')
aided=importlib.util.module_from_spec(spec); spec.loader.exec_module(aided)

VISIBLE=[
'''import XCTest
@testable import ReviewFixture
final class ExistingTests: XCTestCase {
 @MainActor func testSingleWindowSelectsAndRestores() async {
  let window = AppServices().makeWindow()
  window.select("A"); XCTAssertEqual(window.selection.documentID, "A")
  window.restore(documentID: "B"); XCTAssertEqual(window.selection.documentID, "B")
 }
}
''',
'''import XCTest
@testable import ReviewFixture
actor ExistingScheduler: RefreshScheduling { func submit() async throws {} }
actor ExistingAPI: CatalogueFetching { func fetch() async throws -> [String] { ["current"] } }
final class ExistingTests: XCTestCase {
 @MainActor func testInitialForegroundLoadsCatalogue() async {
  let model = RefreshCoordinator(scheduler: ExistingScheduler(), service: ExistingAPI())
  await model.enteredForeground(); XCTAssertEqual(model.items,["current"])
 }
}
''',
'''import XCTest
import Foundation
@testable import ReviewFixture
actor ExistingTransport: SummaryTransport {
 func enqueue(_ payload: Data) async {}
 func sendInteractive(_ payload: Data) async throws {}
}
actor ExistingStore: PendingWorkouts {
 var records: [Workout] = []
 func save(_ workout: Workout) async throws { records.append(workout) }
 func all() async throws -> [Workout] { records }
 func remove(id: String) async throws { records.removeAll { $0.id == id } }
}
final class ExistingTests: XCTestCase {
 func testCompletionRetainsRecordUntilAcknowledgement() async throws {
  let store = ExistingStore(), delivery = WorkoutDelivery(transport: ExistingTransport(),pending: store)
  try await delivery.completed(Workout(id:"17",seconds:30))
  let saved = try await store.all(); XCTAssertEqual(saved.count,1)
  try await delivery.importedAcknowledgement(id:"17")
  let remaining = try await store.all(); XCTAssertTrue(remaining.isEmpty)
 }
}
''',
'''import XCTest
@testable import ReviewFixture
final class ExistingTests: XCTestCase {
 func testCredentialIsNotSynchronizable() { XCTAssertFalse(CredentialPolicy().synchronizable) }
}
''',
'''import XCTest
import Foundation
@testable import ReviewFixture
final class ExistingTests: XCTestCase {
 func testProfileConstructsAndRoundTripsItsCurrentEncoding() throws {
  let original = ProfileDTO(id:"7",displayName:"Mina")
  let decoded = try JSONDecoder().decode(ProfileDTO.self,from:JSONEncoder().encode(original))
  XCTAssertEqual(ProfilePresentation(profile:decoded).title,"Mina")
 }
}
''']
# Outcome-based hidden tests assert independent product behavior, not exact lines or enum values.
HIDDEN_SCENE='''import XCTest
@testable import ReviewFixture
final class HiddenOutcomeTests: XCTestCase {
 @MainActor func testSelectingAndRestoringOneSceneDoesNotChangeOthers() async {
  let app = AppServices(); let a = app.makeWindow(); let b = app.makeWindow(); let c = app.makeWindow()
  a.select("A"); b.restore(documentID:"B")
  XCTAssertEqual(a.selection.documentID,"A"); XCTAssertEqual(b.selection.documentID,"B"); XCTAssertNil(c.selection.documentID)
  b.restore(documentID:nil); XCTAssertEqual(a.selection.documentID,"A")
  XCTAssertTrue(a.catalogue === b.catalogue)
 }
}
'''
HIDDEN_BACKGROUND='''import XCTest
@testable import ReviewFixture
actor HiddenScheduler: RefreshScheduling { func submit() async throws {} }
actor HiddenAPI: CatalogueFetching {
 var failures = 1
 func fetch() async throws -> [String] { if failures > 0 { failures -= 1; throw Offline() }; return ["fresh"] }
 struct Offline: Error {}
}
final class HiddenOutcomeTests: XCTestCase {
 @MainActor func testForegroundRecoversAfterUnexecutedRequestAndFetchFailure() async {
  let model = RefreshCoordinator(scheduler:HiddenScheduler(),service:HiddenAPI())
  await model.scheduleNextRefresh() // No background delivery occurs.
  await model.enteredForeground(); XCTAssertNotNil(model.errorMessage)
  await model.enteredForeground(); XCTAssertEqual(model.items,["fresh"]); XCTAssertNil(model.errorMessage)
 }
}
'''
HIDDEN_WATCH='''import XCTest
import Foundation
@testable import ReviewFixture
actor HiddenTransport: SummaryTransport {
 var waiting: [Data] = []; var imported: Set<String> = []
 func enqueue(_ payload: Data) async { waiting.append(payload) }
 func sendInteractive(_ payload: Data) async throws { throw Unreachable() }
 func phoneBecomesAvailable() throws {
  for data in waiting { imported.insert(try JSONDecoder().decode(Workout.self,from:data).id) }
  waiting.removeAll()
 }
 struct Unreachable: Error {}
}
actor HiddenStore: PendingWorkouts {
 var values: [String:Workout] = [:]
 func save(_ workout: Workout) async throws { values[workout.id] = workout }
 func all() async throws -> [Workout] { Array(values.values) }
 func remove(id: String) async throws { values.removeValue(forKey:id) }
}
final class HiddenOutcomeTests: XCTestCase {
 func testUnavailablePhoneLaterImportsWithoutAnotherWatchActivation() async throws {
  let transport = HiddenTransport(); let store = HiddenStore()
  let delivery = WorkoutDelivery(transport:transport,pending:store)
  try await delivery.completed(Workout(id:"event-9",seconds:60))
  try await transport.phoneBecomesAvailable() // No later delivery.flush or watch activation.
  let received = await transport.imported; XCTAssertEqual(received,["event-9"])
  let retained = try await store.all(); XCTAssertEqual(retained.count,1)
  try await delivery.importedAcknowledgement(id:"event-9")
  let remaining = try await store.all(); XCTAssertTrue(remaining.isEmpty)
 }
}
'''
HIDDEN_API='''import XCTest
import Foundation
@testable import ReviewFixture
final class HiddenOutcomeTests: XCTestCase {
 func testPreviouslyCachedAndNewServerProfilesBothRenderSameName() throws {
  for json in [#"{"id":"7","name":"Mina"}"#,#"{"id":"7","display_name":"Mina"}"#] {
   let profile = try JSONDecoder().decode(ProfileDTO.self,from:Data(json.utf8))
   XCTAssertEqual(ProfilePresentation(profile:profile).title,"Mina")
   let encoded = try JSONSerialization.jsonObject(with:JSONEncoder().encode(profile)) as! [String:String]
   XCTAssertEqual(encoded["display_name"],"Mina"); XCTAssertNil(encoded["name"])
  }
 }
}
'''

def main():
 parser=argparse.ArgumentParser(); parser.add_argument('destination',type=Path); args=parser.parse_args(); root=fresh(args.destination)
 aided.populate_variants(); cases=copy.deepcopy(aided.CASES[:5]); hidden=[HIDDEN_SCENE,HIDDEN_BACKGROUND,HIDDEN_WATCH,None,HIDDEN_API]
 manifest=[]; oracle=[]
 for number,case in enumerate(cases,1):
  repo=root/'repositories'/f'component-{number:02d}'
  files={'Package.swift':aided.PACKAGE,'.gitignore':'.build/\n','README.md':aided.COMMON.replace('Tests are existing smoke coverage unless their names state otherwise.','Run `swift build` and `swift test` for the portable module. Existing tests cover established happy paths; platform adapters are unchanged.'),'PRODUCT.md':'# '+case['title']+'\n\n'+case['requirements'],**case['base'],'Tests/ReviewFixtureTests/ExistingTests.swift':VISIBLE[number-1]}
  # The API base uses old-name encoding; current roundtrip is green on both contracts.
  base=init(repo,files); variants={}
  for variant in ['clean','defect']:
   git(repo,'switch','--quiet','-c','snapshot-'+str(len(variants)+1),base)
   delta={p:c for p,c in case[variant].items() if not p.startswith('Tests/')}
   write(repo,delta); variants[variant]=commit(repo,case['title'])
  git(repo,'switch','--quiet','--detach',variants['clean'])
  test_path=None
  if hidden[number-1]:
   test_path=root/'evaluator'/'hidden'/f'component-{number:02d}.swift'; write(root,{str(test_path.relative_to(root)):hidden[number-1]})
  manifest.append({'id':case['id'],'repository':str(repo),'base':base,'variants':variants,'hidden_test':str(test_path) if test_path else None,'evaluator_kind':'outcome_test' if test_path else 'static_platform_contract'})
  oracle.append({'id':case['id'],'defect':case['oracle'],'clean_findings':0,'adjudication':aided.EVIDENCE_SCOPE[case['id']],'limits':'Hidden tests are portable product invariants, not Apple adapter/device execution.' if test_path else 'Keychain policy is adjudicated by the actual Security accessibility mapping and explicit lifecycle requirement; no host or simulated test proves lock-state runtime behavior.'})
 save(root/'evaluator/oracle.json',oracle); save(root/'manifest.json',manifest)
 mapping=[]
 for number,(index,variant) in enumerate([(0,'defect'),(0,'clean'),(1,'clean'),(1,'defect'),(2,'defect'),(2,'clean'),(3,'clean'),(3,'defect'),(4,'defect'),(4,'clean')],1):
  row=manifest[index]; path=root/'inputs'/f'input-{number:02d}.md'; write(root,{str(path.relative_to(root)):prompt(row['repository'],row['base'],row['variants'][variant])}); mapping.append({'input':str(path),'id':row['id'],'variant':variant,'base':row['base'],'head':row['variants'][variant]})
 save(root/'evaluator/input-map.json',mapping)
 print(f'Created {len(mapping)} green-visible-suite targets at {root}')
if __name__=='__main__': main()
