nums := #(1 2 3 4 5 6).

'B1:' printNl.
nums printNl.

'B2:' printNl.
nums2 := nums collect: [ :each | each * 2].
nums2 printNl.

'B3:' printNl.
nums3 := nums select: [ :each | each \\ 2 = 0].
nums3 printNl.

'B4:' printNl.
nums4 := nums reject: [ :each | each < 4].
nums4 printNl.

'B5:' printNl.
nums5 := nums inject: 0 into: [ :a :c | a + c].
nums5 printNl.
