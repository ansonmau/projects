VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} ListOrdersForm 
   Caption         =   "List Orders Menu"
   ClientHeight    =   9060.001
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   15225
   OleObjectBlob   =   "ListOrdersForm.frx":0000
   ShowModal       =   0   'False
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "ListOrdersForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public rs As New ADODB.Recordset
Public rs2 As New ADODB.Recordset
Public sqlStr As String

Public GlobalIDVar As Long              ' this is used to pass a variable into the edit userform

Private lastButtonPressed As String     'stores the last button pressed for the refresh sub



Public Sub refreshList()
    If lastButtonPressed = "" Then
        Exit Sub
    ElseIf lastButtonPressed = "all active orders" Then
        Call AllActiveOrdersButton_Click
    ElseIf lastButtonPressed = "all orders" Then
        Call AllOrdersButton_Click
    ElseIf lastButtonPressed = "30 days" Then
        Call PastThirtyButton_Click
    ElseIf lastButtonPressed = "60 days" Then
        Call PastSixtyButton_Click
    ElseIf lastButtonPressed = "search" Then
        Call SearchButton_Click
    Else
        Exit Sub
    End If
End Sub

Private Sub AddOrderButton_Click()
    NewOrderForm.Show
    
    refreshList
End Sub

Private Sub AllActiveOrdersButton_Click()
    Dim li As ListItem
    InfoBox.ListItems.Clear
    sqlStr = "SELECT * FROM [Orders], [OrderStatus]" & _
    " WHERE [Orders].[ACTIVE] = True" & _
    " AND [Orders].[ID] = [OrderStatus].[ID]" & _
    " ORDER BY [Orders].[ID] DESC"
    rs.Open sqlStr, OrderMain.cn
    
    addToList rs
    
    rs.Close
    lastButtonPressed = "all active orders"
End Sub


Private Sub EditButton_Click()
    If Not InfoBox.SelectedItem Is Nothing Then
        GlobalIDVar = InfoBox.SelectedItem
        EditOrderForm.Show vbModeless
    Else
        
    End If
    
End Sub


Private Sub InfoBox_ColumnClick(ByVal ColumnHeader As MSComctlLib.ColumnHeader)
    With InfoBox
        .SortKey = ColumnHeader.Index - 1
        If .SortOrder = lvwAscending Then
            .SortOrder = lvwDescending
        Else
            .SortOrder = lvwAscending
        End If
        .Sorted = True
    End With
End Sub


Private Sub AllOrdersButton_Click()
    Dim li As ListItem
    
    InfoBox.ListItems.Clear
    
    sqlStr = "SELECT * FROM [Orders], [OrderStatus]" & _
    " WHERE [Orders].[ID] = [OrderStatus].[ID]" & _
    " ORDER BY [Orders].[ID] DESC"
    
    rs.Open sqlStr, OrderMain.cn
    
    addToList rs
    
    rs.Close
    
    lastButtonPressed = "all orders"
    
End Sub

Private Sub CancelButton_Click()
    Unload Me
End Sub


Private Sub InfoBox_DblClick()
    Call EditButton_Click
End Sub

Private Sub PastSixtyButton_Click()
    Dim li As ListItem
    
    InfoBox.ListItems.Clear
    sqlStr = "SELECT * FROM [Orders], [OrderStatus] WHERE [Orders].[ACTIVE] = True AND [Orders].[OrderDate] > #" & DateAdd("d", -60, Date) & "#" & _
    " AND [Orders].[ID] = [OrderStatus].[ID]" & _
    " ORDER BY [Orders].[ID] DESC"
    
    rs.Open sqlStr, OrderMain.cn
    
    addToList rs
    
    rs.Close
    
    lastButtonPressed = "60 days"
End Sub

Private Sub PastThirtyButton_Click()
    Dim li As ListItem
    
    InfoBox.ListItems.Clear
    
    sqlStr = "SELECT * FROM [Orders], [OrderStatus] WHERE [Orders].[ACTIVE] = True AND [Orders].[OrderDate] > #" & DateAdd("d", -30, Date) & "#" & _
    " AND [Orders].[ID] = [OrderStatus].[ID]" & _
    " ORDER BY [Orders].[ID] DESC"
    
    rs.Open sqlStr, OrderMain.cn
        
    addToList rs
        
    rs.Close
    
    lastButtonPressed = "30 days"
    
End Sub


Private Sub RefreshButton_Click()
    Call refreshList
End Sub

Private Sub ResizeButton_Click()
    Call resize_stuff
End Sub

Private Sub SearchButton_Click()
    Dim sqlStrTemp As String
    
    InfoBox.ListItems.Clear
    
    sqlStr = "SELECT * FROM [Orders], [OrderStatus] WHERE [Orders].[ACTIVE] = True"
    
    If FindIDBox.Value <> "" Then
        sqlStr = sqlStr & " AND [Orders].[ID] = " & FindIDBox.Value
    End If
    
    If FindDescriptionBox.Value <> "" Then
        sqlStr = sqlStr & " AND [Orders].[ItemDescription] LIKE '%" & FindDescriptionBox.Value & "%'"
    End If
    
    If FindPOBox.Value <> "" Then
        sqlStrTemp = "SELECT [ID] FROM [OrderStatus] WHERE [OrderStatus].[PONum] = '" & FindPOBox.Value & "'"
        rs.Open sqlStrTemp, OrderMain.cn
        
        If Not rs.EOF Then
            sqlStr = sqlStr & " AND ([ID] = " & rs.Fields("ID")                     'back to the original sqlStr querying the Orders table
            rs.MoveNext
            Do Until rs.EOF
                sqlStr = sqlStr & " OR [ID] = " & rs.Fields("ID")                   'back to the original sqlStr querying the Orders table
                rs.MoveNext
            Loop
            sqlStr = sqlStr & ")"                                                   'close off the bracket created after the AND 5 lines up
        Else
            sqlStr = sqlStr & " AND [ID] = 0"                                       'bandaid fix in order to show nothing to user if they search for something that does not exist
                                                                                    'Without this, if user searches something that does not exist, all ACTIVE orders will show.
        End If
        rs.Close
    End If
    
    If FindVendorBox.Value <> "" Then
        sqlStrTemp = "SELECT [ID] FROM [OrderStatus] WHERE [VendorName] LIKE '%" & FindVendorBox.Value & "%'"
        rs.Open sqlStrTemp, OrderMain.cn
        
        If Not rs.EOF Then
            sqlStr = sqlStr & " AND ([ID] = " & rs.Fields("ID")                     'back to the original sqlStr querying the Orders table
            rs.MoveNext
            Do Until rs.EOF
                sqlStr = sqlStr & " OR [ID] = " & rs.Fields("ID")                   'back to the original sqlStr querying the Orders table
                rs.MoveNext
            Loop
            sqlStr = sqlStr & ")"                                                   'close off the bracket created after the AND 5 lines up
        Else
            sqlStr = sqlStr & " AND [ID] = 0"                                       'bandaid fix in order to show nothing to user if they search for something that does not exist
                                                                                    'Without this, if user searches something that does not exist, all ACTIVE orders will show.
        End If
        rs.Close
    End If
    
    sqlStr = sqlStr & " ORDER BY [Orders].[ID] DESC"
    
    rs.Open sqlStr, OrderMain.cn
    
    addToList rs
    
    rs.Close
    
    lastButtonPressed = "search"
End Sub

Private Sub addToList(rs As Recordset)
    Dim li As ListItem
    
    Do Until rs.EOF
        Set li = Me.InfoBox.ListItems.Add(, , rs.Fields("Orders.ID"))
        li.ListSubItems.Add , , CStr(rs.Fields("OrderDate"))
        li.ListSubItems.Add , , rs.Fields("SalesName")
        li.ListSubItems.Add , , rs.Fields("ItemDescription")
        li.ListSubItems.Add , , rs.Fields("Orders.ItemQuantity")
        li.ListSubItems.Add , , Replace(rs.Fields("Remarks"), "\n", "    ")
        li.ListSubItems.Add , , rs.Fields("WHStatus")
        li.ListSubItems.Item(6).ForeColor = RGB(0, 0, 255)
        li.ListSubItems.Add , , CStr(rs.Fields("PONum"))
        li.ListSubItems.Add , , rs.Fields("VendorName")
        li.ListSubItems.Add , , rs.Fields("OrderStatus.ItemQuantity")
        li.ListSubItems.Add , , CStr(rs.Fields("UnitCost")) & " " & rs.Fields("CurrencyType")
        li.ListSubItems.Add , , rs.Fields("ShippingCost") & " " & rs.Fields("ShippingCostCurrencyType")
        If rs.Fields("ACTIVE") = True Then
            li.ListSubItems.Add , , "YES"
        Else
            li.ListSubItems.Add , , "NO"
        End If
        rs.MoveNext
    Loop

End Sub

Private Sub userform_activate()

    Call ResizeModule.MakeFormResizable
    
End Sub

Private Sub resize_stuff()
    Dim windowH As Integer
    Dim windowW As Integer

    windowW = Me.Width
    windowH = Me.Height
    
    InfoBox.Width = windowW - 131                           'these numbers are all offsets to keep them to the same ratio as before the resize.
    InfoBox.Height = windowH - 110
    
    CancelButton.Top = windowH - 68
    CancelButton.Width = Me.Width
    
    RefreshButton.Left = InfoBox.Width + 48
    
End Sub

Private Sub UserForm_initialize()
    
    Me.InfoBox.ColumnHeaders.Add Text:="ID", Width:=54                                  'add all the columns and their names
    Me.InfoBox.ColumnHeaders.Add Text:="Order Date", Width:=57
    Me.InfoBox.ColumnHeaders.Add Text:="Sales Name", Width:=60
    Me.InfoBox.ColumnHeaders.Add Text:="Item Description", Width:=200
    Me.InfoBox.ColumnHeaders.Add Text:="Item Quantity", Width:=50
    Me.InfoBox.ColumnHeaders.Add Text:="Remarks", Width:=175
    Me.InfoBox.ColumnHeaders.Add Text:="WH Status", Width:=110
    Me.InfoBox.ColumnHeaders.Add Text:="PO#", Width:=50
    Me.InfoBox.ColumnHeaders.Add Text:="Vendor", Width:=65
    Me.InfoBox.ColumnHeaders.Add Text:="Recieved Quantity", Width:=50
    Me.InfoBox.ColumnHeaders.Add Text:="Unit Cost", Width:=70
    Me.InfoBox.ColumnHeaders.Add Text:="Shipping Cost", Width:=70
    Me.InfoBox.ColumnHeaders.Add Text:="Active", Width:=45
    
    Me.InfoBox.FullRowSelect = True
    Me.InfoBox.LabelEdit = lvwManual                                                    'makes it so that the user can't edit information on the list (this would be client side only anyways...)
    
    Me.CancelButton.Width = Me.Width                                                    'resize cancel button
    
    Call AllActiveOrdersButton_Click                                                    'default to all active orders when the form is opened.
    
End Sub
