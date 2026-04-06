"
Repeated pattern found in the grading workflow:
  - select: keep only items that meet a minimum threshold (passing scores >= 50)
  - reject: drop items that exceed a maximum threshold (suspicious scores > 100)
  - inject:into: reduce the remaining items to a single total
This three-step clean-and-total idiom repeats across several tools,
so we give it one clear name: totalOfCleanScores:
"

Object subclass: #ScoreTools.

ScoreTools class extend [
    totalOfCleanScores: aCollection [
        | passing valid |
        passing := aCollection select: [ :each | each >= 50 ].
        valid   := passing reject:  [ :each | each > 100 ].
        ^ valid inject: 0 into: [ :acc :each | acc + each ]
    ]
]

"--- use site ---"
| scores cleanedTotal |
scores := #(20 55 70 101 85 49 100 200).
cleanedTotal := ScoreTools totalOfCleanScores: scores.
cleanedTotal printNl.
