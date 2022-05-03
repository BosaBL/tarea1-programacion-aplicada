import wx
import wx.grid as gridlib
import wx.lib.masked as masked


from controller.ClientController import ClientController
from controller.DatabaseController import DatabaseController
from controller.NodeListController import NodeListController


class App(wx.App):
    def __init__(self):
        wx.App.__init__(self)

        MainFrame()

        self.MainLoop()


# Main Frame
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            title="Client Maintainer",
            size=(500, 600),
            style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
        )

        self.__panelSplitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.__panelSplitter.SetSashInvisible(True)

        self.clientListPanel = ClientListPanel(self.__panelSplitter)
        self.clientListControlPanel = ClientListControlPanel(
            self.__panelSplitter, self.clientListPanel
        )

        self.__panelSplitter.SplitHorizontally(
            self.clientListPanel, self.clientListControlPanel
        )

        self.__panelSplitter.SetMinimumPaneSize(300)

        self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__sizer.Add(self.__panelSplitter, 0, wx.EXPAND | wx.ALL | wx.BOTTOM, 3)
        self.__h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__h_sizer.AddSpacer(3)

        self.__sizer.Add(self.__h_sizer)
        self.SetSizer(self.__sizer)

        self.Show()


class ClientListPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        # Setting font for better readability
        self.__font = wx.Font(
            10,
            family=wx.FONTFAMILY_MODERN,
            style=0,
            weight=90,
            underline=False,
            faceName="",
            encoding=wx.FONTENCODING_DEFAULT,
        )

        # Controllers used for displaying the client on the grid, they must be public for later usage
        self.databaseController = DatabaseController()
        self.nodeListController = NodeListController()
        self.clientController = ClientController()
        self.databaseController.populateDatabase()
        self.clientList = self.databaseController.getClient("clients.csv")

        # Setting up grid
        self.__clientGrid = gridlib.Grid(self)
        self.__clientGrid.CreateGrid(0, 2)
        self.__clientGrid.SetRowLabelSize(0)
        self.__clientGrid.SetColLabelValue(0, "Nombre")
        self.__clientGrid.SetColLabelValue(1, "D.N.I")
        self.__clientGrid.EnableDragColSize(False)
        self.__clientGrid.SetColLabelAlignment(
            horiz=wx.ALIGN_CENTRE, vert=wx.ALIGN_CENTRE
        )
        self.__clientGrid.SetDefaultCellAlignment(horiz=wx.LEFT, vert=wx.ALIGN_BOTTOM)
        self.__clientGrid.SetDefaultCellFont(self.__font)

        self.__clientGrid.EnableEditing(False)

        self.loadClients()

        # Resizing rows and columns to fit its content (not time efficient as it needs to re-iterate the grid)
        self.__clientGrid.AutoSizeColumns()
        self.__clientGrid.AutoSizeRows()

        # Sizing grid to the panel size.
        self.__sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__sizer.Add(self.__clientGrid, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(self.__sizer)

    # Loading clients on the grid.
    def loadClients(self):
        self.clearClients()
        if self.clientList:
            self.__clientGrid.AppendRows(numRows=len(self.clientList.printList()))
            for idx, client in enumerate(self.clientList.printList()):
                self.__clientGrid.SetCellValue(idx, 0, client.getName())
                self.__clientGrid.SetCellValue(idx, 1, client.getDni())
                self.__clientGrid.AutoSizeRow(idx)
        else:
            self.__clientGrid.AppendRows(numRows=1)
            self.__clientGrid.SetCellValue(0, 0, "Empty List")
            self.__clientGrid.SetCellValue(0, 1, "EmptyList")

    def clearClients(self):
        if self.__clientGrid.GetNumberRows() != 0:
            self.__clientGrid.DeleteRows(0, self.__clientGrid.GetNumberRows())


class ClientListControlPanel(wx.Panel):
    def __init__(self, parent, listPanel):
        wx.Panel.__init__(self, parent=parent)

        self.__listPanel = listPanel

        self.__font = wx.Font(
            10,
            family=wx.FONTFAMILY_MODERN,
            style=1,
            weight=90,
            underline=False,
            faceName="",
            encoding=wx.FONTENCODING_DEFAULT,
        )
        self.SetFont(self.__font)
        self.__gridsizer = wx.GridBagSizer(5, 5)

        # Add Client
        self.__ClientBox = wx.StaticBox(self, label="Añadir Cliente")
        self.__ClientBoxSizer = wx.StaticBoxSizer(self.__ClientBox, wx.VERTICAL)
        self.__ClientBoxGrid = wx.GridBagSizer(6, 6)
        self.__ClientBoxGrid.Add(
            wx.StaticText(self, label="NOMBRE:"), pos=(0, 0), flag=wx.ALIGN_CENTER
        )
        self.__nameAddEntry = wx.TextCtrl(
            self, style=wx.TE_LEFT, name="nameAddEntry", size=(150, 20)
        )
        self.__ClientBoxGrid.Add(
            self.__nameAddEntry,
            pos=(0, 1),
        )
        self.__ClientBoxGrid.Add(
            wx.StaticText(self, label="DNI:"),
            pos=(1, 0),
            flag=wx.ALIGN_RIGHT,
        )
        self.__dniAddEntry = masked.TextCtrl(
            self,
            style=wx.TE_LEFT,
            name="dniAddEntry",
            mask="########-#",
        )
        self.__ClientBoxGrid.Add(
            self.__dniAddEntry,
            pos=(1, 1),
        )
        self.__addButton = wx.Button(self, label="Añadir")
        self.__ClientBoxGrid.Add(self.__addButton, pos=(2, 1), flag=wx.ALIGN_RIGHT)

        self.__ClientBoxSizer.Add(self.__ClientBoxGrid)
        self.__gridsizer.Add(self.__ClientBoxSizer, pos=(1, 1), flag=wx.EXPAND | wx.ALL)

        # Search Client
        self.__SearchClientBox = wx.StaticBox(self, label="Buscar Cliente")
        self.__SearchClientBoxSizer = wx.StaticBoxSizer(
            self.__SearchClientBox, wx.VERTICAL
        )
        self.__SearchClientBoxGrid = wx.GridBagSizer(6, 6)
        self.__SearchClientBoxGrid.Add(
            wx.StaticText(self, label="DNI:"),
            pos=(0, 0),
            flag=wx.ALIGN_CENTER,
        )
        self.__dniSearchEntry = masked.TextCtrl(
            self,
            style=wx.TE_LEFT,
            name="dniSearchEntry",
            mask="########-#",
        )
        self.__SearchClientBoxGrid.Add(
            self.__dniSearchEntry,
            pos=(0, 1),
        )
        self.__searchButton = wx.Button(self, label="Buscar")
        self.__SearchClientBoxGrid.Add(
            self.__searchButton, pos=(2, 1), flag=wx.ALIGN_RIGHT
        )

        self.__SearchClientBoxSizer.Add(self.__SearchClientBoxGrid)
        self.__gridsizer.Add(
            self.__SearchClientBoxSizer, pos=(1, 2), flag=wx.EXPAND | wx.ALL
        )

        # Delete Client
        self.__DeleteClientBox = wx.StaticBox(self, label="Eliminar Cliente")
        self.__DeleteClientBoxSizer = wx.StaticBoxSizer(
            self.__DeleteClientBox, wx.VERTICAL
        )
        self.__DeleteClientBoxGrid = wx.GridBagSizer(6, 6)
        self.__DeleteClientBoxGrid.Add(
            wx.StaticText(self, label="DNI:"),
            pos=(0, 0),
            flag=wx.ALIGN_CENTER,
        )
        self.__dniDeleteEntry = masked.TextCtrl(
            self,
            style=wx.TE_LEFT,
            name="dniDeleteEntry",
            mask="########-#",
        )
        self.__DeleteClientBoxGrid.Add(
            self.__dniDeleteEntry,
            pos=(0, 1),
        )
        self.__deleteButton = wx.Button(self, label="Eliminar")
        self.__DeleteClientBoxGrid.Add(
            self.__deleteButton, pos=(2, 1), flag=wx.ALIGN_RIGHT
        )

        self.__DeleteClientBoxSizer.Add(self.__DeleteClientBoxGrid)
        self.__gridsizer.Add(self.__DeleteClientBoxSizer, pos=(2, 1), flag=wx.CENTER)

        # Change Client Name
        self.__ChangeNameBox = wx.StaticBox(self, label="Actualizar Cliente")
        self.__ChangeNameBoxSizer = wx.StaticBoxSizer(self.__ChangeNameBox, wx.VERTICAL)
        self.__ChangeNameBoxGrid = wx.GridBagSizer(6, 6)

        self.__dniChangeNameEntry = masked.TextCtrl(
            self, style=wx.TE_LEFT, name="dniChangeNameEntry", mask="########-#"
        )

        self.__ChangeNameBoxGrid.Add(
            wx.StaticText(self, label="DNI:"),
            pos=(0, 0),
            flag=wx.ALIGN_CENTER,
        )

        self.__ChangeNameBoxGrid.Add(
            self.__dniChangeNameEntry,
            pos=(0, 1),
        )
        self.__changeNameButton = wx.Button(self, label="Cambiar")
        self.__ChangeNameBoxGrid.Add(
            self.__changeNameButton, pos=(2, 1), flag=wx.ALIGN_RIGHT
        )

        self.__ChangeNameBoxSizer.Add(self.__ChangeNameBoxGrid)
        self.__gridsizer.Add(
            self.__ChangeNameBoxSizer, pos=(2, 2), flag=wx.CENTER | wx.EXPAND
        )

        self.SetSizer(self.__gridsizer)

        # Button Event Handling
        self.__addButton.Bind(wx.EVT_BUTTON, self.addClient)
        self.__searchButton.Bind(wx.EVT_BUTTON, self.searchClient)
        self.__deleteButton.Bind(wx.EVT_BUTTON, self.deleteClient)
        self.__changeNameButton.Bind(wx.EVT_BUTTON, self.changeName)

    def invalidDniDiag(self):
        diag = wx.MessageDialog(
            self, "Tienes que ingresar un DNI válido", "ERROR", wx.ICON_ERROR
        )
        diag.ShowModal()
        diag.Destroy()

    def clearEntry(self, entry):
        entry.SetValue("")

    # Add Client
    def addClient(self, e):
        dniEntry = self.__dniAddEntry.GetLineText(0)
        nameEntry = self.__nameAddEntry.GetLineText(0)
        self.clearEntry(self.__dniAddEntry)
        self.clearEntry(self.__nameAddEntry)
        # Delete every white space to verify DNI.
        if len(dniEntry.replace(" ", "")) != 10:
            self.invalidDniDiag()
        # Check for valid name.
        elif len(nameEntry) == 0:
            diag = wx.MessageDialog(
                self, "Tienes que ingresar un Nombre", "ERROR", wx.ICON_ERROR
            )
            diag.ShowModal()
            diag.Destroy()
        else:
            listPanel = self.__listPanel
            if not listPanel.clientList.searchByDni(dniEntry):
                listPanel.clientList.addNode(
                    listPanel.clientController.createClient(
                        dniEntry,
                        nameEntry,
                    )
                )
                listPanel.loadClients()
                diag = wx.MessageDialog(
                    self, "Cliente Añadido con Éxito", "OPERACION EXITOSA", wx.OK
                )
                diag.ShowModal()
                diag.Destroy()
            else:
                diag = wx.MessageDialog(
                    self, "Ya existe un cliente con ese DNI", "ERROR", wx.ICON_ERROR
                )
                diag.ShowModal()
                diag.Destroy()

    def searchClient(self, e):
        dniEntry = self.__dniSearchEntry.GetLineText(0)
        self.clearEntry(self.__dniSearchEntry)
        if len(dniEntry.replace(" ", "")) != 10:
            self.invalidDniDiag()
        elif self.__listPanel.clientList.searchByDni(dniEntry):
            client = self.__listPanel.clientList.searchByDni(dniEntry)
            diag = wx.MessageDialog(
                self,
                f"Nombre: {client.getName()}\nD.N.I: {client.getDni()}",
                "Cliente Encontrado",
                wx.OK,
            )
            diag.ShowModal()
            diag.Destroy()
        else:
            diag = wx.MessageDialog(
                self, "Cliente no encontrado", "ERROR", wx.ICON_ERROR
            )
            diag.ShowModal()
            diag.Destroy()

    def deleteClient(self, e):
        dniEntry = self.__dniDeleteEntry.GetLineText(0)
        self.clearEntry(self.__dniDeleteEntry)
        if len(dniEntry.replace(" ", "")) != 10:
            self.invalidDniDiag()
        elif self.__listPanel.clientList.searchByDni(dniEntry):
            self.__listPanel.clientList.deleteNode(dniEntry)
            self.__listPanel.loadClients()
        else:
            diag = wx.MessageDialog(
                self, "Cliente no encontrado", "ERROR", wx.ICON_ERROR
            )
            diag.ShowModal()
            diag.Destroy()

    def changeName(self, e):
        dniEntry = self.__dniChangeNameEntry.GetLineText(0)
        self.clearEntry(self.__dniChangeNameEntry)
        if len(dniEntry.replace(" ", "")) != 10:
            self.invalidDniDiag()
        elif self.__listPanel.clientList.searchByDni(dniEntry):
            client = self.__listPanel.clientList.searchByDni(dniEntry)

            # Setting up new dialog box for new name entry
            diag = wx.Dialog(self, title="Actualizar Cliente")

            diagGrid = wx.GridBagSizer(10, 5)

            updateBox = wx.StaticBox(diag, label="ACTUALIZAR NOMBRE")

            updateBoxSizer = wx.StaticBoxSizer(updateBox, wx.VERTICAL)

            nameLabel = wx.StaticText(updateBox, label="NOMBRE:")
            nameEntry = wx.TextCtrl(updateBox, size=(150, 20), style=wx.TE_LEFT)
            nameButton = wx.Button(updateBox, label="Actualizar", style=wx.ALIGN_RIGHT)

            diagGrid.Add(nameButton, pos=(1, 1))
            diagGrid.Add(nameLabel, pos=(0, 0))
            diagGrid.Add(nameEntry, pos=(0, 1))

            updateBoxSizer.Add(diagGrid)
            diag.SetSizer(updateBoxSizer)

            # updater function, also closes the dialog on successfull update
            def updateName(e):
                newName = nameEntry.GetLineText(0)
                client.setName(newName)

                newdiag = wx.MessageDialog(
                    self, "EXITO", "El cliente se ha actualizado exitosamente", wx.OK
                )
                newdiag.ShowModal()
                newdiag.Destroy()

                diag.Destroy()

            nameButton.Bind(wx.EVT_BUTTON, updateName)

            diag.ShowModal()

            self.__listPanel.loadClients()
        else:
            diag = wx.MessageDialog(
                self, "Cliente no encontrado", "ERROR", wx.ICON_ERROR
            )
            diag.ShowModal()
            diag.Destroy()


if __name__ == "__main__":
    app = App()
