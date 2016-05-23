Attribute VB_Name = "Module1"
Sub FindFootnoteStyle()
    Dim rngFT As Word.Range

    Set rngFT = ActiveDocument.StoryRanges(wdFootnotesStory)
    With rngFT.Find
      FindTextStyle
    End With
End Sub

Sub FindTextStyle()
    Dim strStyle As String
    strStyle = "Subtle Reference"
    ' Selection.HomeKey Unit:=wdStory
        With Selection.Find
        .text = ""
        .ClearFormatting
        .Style = strStyle
            Do While .Execute
            ActiveDocument.Hyperlinks.Add Anchor:=Selection.Range, _
            Address:="http://www.httpstat.us/404"
            Selection.Style = ActiveDocument.Styles("Normal")
            Loop
        End With
End Sub




