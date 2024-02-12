Sub MergeSameCells()
'THIS CODE WAS ADAPTED FROM SOURCE: https://www.extendoffice.com/documents/excel/1138-excel-merge-same-value.html
'Source was accessed on 10.12.2023.
Dim Rng As Range, xCell As Range
Dim xRows As Long
xTitleId = "KutoolsforExcel"
Set WorkRng = Application.Selection
Set WorkRng = Application.InputBox("Range", xTitleId, WorkRng.Address, Type:=8)
Application.ScreenUpdating = False
Application.DisplayAlerts = False
xRows = WorkRng.Rows.Count
For Each Rng In WorkRng.Columns
    For i = 1 To xRows - 1
        For j = i + 1 To xRows
            If Rng.Cells(i, 1).Value <> Rng.Cells(j, 1).Value Then
                Exit For
            End If
        Next
        WorkRng.Parent.Range(Rng.Cells(i, 1), Rng.Cells(j - 1, 1)).Merge
        i = j - 1
    Next
Next
Application.DisplayAlerts = True
Application.ScreenUpdating = True
End Sub