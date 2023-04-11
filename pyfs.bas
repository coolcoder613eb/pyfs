#include "fbgfx.bi"  ' Include FreeBASIC graphics library
#include "fbstring.bi"  ' Include FreeBASIC string library

Type FileData
    filename As String
    length As Integer
    data() As Byte
End Type

Dim As String fmt = "=I"

Function get_str(inbytes() As Byte, Optional index As Integer = 0) As String
    Dim As Byte byte = inbytes(index)
    Dim As String data = ""
    While byte <> 0
        index += 1
        data += Chr(byte)
        byte = inbytes(index)
    Wend

    Return data
End Function

Sub writeimg(filedir As String = "testfiles", imgfile As String = "pyfs.img")
    Dim As String cwd = CurDir()
    Dim As FileData files()
    ChDir(filedir)
    Dim As String filename
    Dim As ULongInt length
    Dim As String read
    Dim As FileData file
    Dim As Integer f
    Dim As Byte b
    For Each filename In Dir
        On Error Resume Next
        f = FreeFile
        Open filename For Binary As #f
        If Err = 0 Then
            length = LOF(f)
            ReDim file.data(length - 1)
            Get #f, , file.data
            Close #f
            file.filename = filename + Chr(0)
            file.length = length
            files.Append file
        End If
        On Error GoTo 0
    Next
    Dim As ULongInt i
    Dim As ULongInt j
    Dim As ULongInt k
    Dim As ULongInt dataSize
    For i = 0 To UBound(files)
        dataSize = Len(files(i).filename) + 4 + files(i).length
        ReDim file.data(dataSize - 1)
        k = 0
        For j = 0 To Len(files(i).filename) - 1
            file.data(k) = Asc(files(i).filename[j])
            k += 1
        Next
        file.data(k) = 0
        k += 1
        file.length = files(i).length
        For j = 0 To 3
            file.data(k) = (files(i).length Shr (8 * (3 - j))) And 255
            k += 1
        Next
        For j = 0 To files(i).length - 1
            file.data(k) = files(i).data(j)
            k += 1
        Next
        files(i) = file
    Next
    Dim As ULongInt totalSize
    totalSize = 0
    For i = 0 To UBound(files)
        totalSize += UBound(files(i).data) + 1
    Next
    ReDim file.data(totalSize - 1)
    k = 0
    For i = 0 To UBound(files)
        For j = 0 To UBound(files(i).data)
            file.data(k) = files(i).data(j)
            k += 1
        Next
    Next
    ChDir(cwd)
    f = FreeFile
    Open imgfile For Binary As #f
    Put #f, , file.data
    Close #f
End Sub

Sub readimg(filedir As String = "testread", imgfile As String = "pyfs.img")
    Dim As String cwd = CurDir()
    Dim As FileData files()
    Dim As String read
    Dim As U

LongInt dataSize
Dim As FileData file
Dim As Integer f
Dim As Byte b
f = FreeFile
Open imgfile For Binary As #f
Dim As ULongInt fileSize = LOF(f)
ReDim file.data(fileSize - 1)
Get #f, , file.data
Close #f
Dim As ULongInt i = 0
Dim As ULongInt j = 0
Dim As ULongInt k = 0
While i < fileSize
read = get_str(file.data, i)
i += Len(read) + 1
file.filename = read
file.length = 0
For j = 0 To 3
file.length = (file.length * 256) + file.data(i)
i += 1
Next
ReDim file.data(file.length - 1)
For j = 0 To file.length - 1
file.data(j) = file.data(i)
i += 1
Next
files.Append file
Wend
ChDir(filedir)
For i = 0 To UBound(files)
f = FreeFile
Open files(i).filename For Binary As #f
Put #f, , files(i).data
Close #f
Next
ChDir(cwd)
End Sub

' Example usage:
' Create an image file from files in a directory
writeimg("testfiles", "pyfs.img")

' Read files from an image file and save them to a directory
readimg("testread", "pyfs.img")