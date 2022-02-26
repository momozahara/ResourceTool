import atexit
import binascii
import os
import tempfile
import tkinter as TK
import json
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askokcancel
from tkinter import *
from tkinter.ttk import Treeview

hdata1 = "\
#pragma once\n\
namespace RESOURCE\n\
{\n\
int\
"
hdata2 = "\
// return hex data return empty if not found\n\
std::string GetItem(int id);\n\
// convert hex data to bytes\n\
std::string unhexlify(std::string hex);\n\
}\
"
cppdata1 = "\
#include <iostream>\n\
#include <map>\n\
#include <string>\n\
#include \"resource.h\"\n\
namespace RESOURCE\n\
{\n\
std::map<int, std::string> Items = {\n\
"
cppdata2 = "\
};\n\
std::string GetItem(int id) {\n\
	return Items[id];\n\
}\n\
// unhexlify\n\
std::string unhexlify(std::string hex) {\n\
	std::string ret;\n\
	for (int i = 0; i < hex.size(); i += 2) {\n\
		ret += (char)(std::stoi(hex.substr(i, 2), nullptr, 16));\n\
	}\n\
	return ret;\n\
}\
}\
"

ICON = '00000100010010100000010008006805000016000000280000001000000020000000010008000000000040050000000000000000000000010000000100008c868f0098919b00a097a300918fa4008f9fc90098aede009cb1e20090a4d0009cb1e10097acdb00a0b7ea0095a7cf009697a700a59ca900a49ba7008a858c00938d96009f98a200aea5b200b3a9b800767a920091a3c600b6cbe100b6cbe50098acd1005d6377009f96a500bdb3c200aca4af009c959f00928c960087818a008e87910099929c00a9a1ad00968c960072788300c8dff600aabff200a5baf200c5dcf30064656a00887d8600b9afbd00a29ba500958e98008e8891008a848d00968e9900a49ca7008b8088006a6c7400cee6fe00cbe2fa00a2b6df00a1b5df00cce3f900cbe2f800544f5000a99fac00aaa1ad009b949e00908992009d95a1009e94a0005b5a65009cadc800bed5f700c6defe00cce4fe00c7dffa00c7dffe00c2dafc009caac2005a535800918894009d95a000847c8600786e76005b5a7700635a74007d86b500a0b7fc00a4bbfc00b0c8fb0097ace800a5bcfc00a0b7f800848bb400645e7100655a63006c5f6300938b97004f424100372219006354750073463f006e77ac008da0e90093a8fa008ca0e50091a6f20096abf90096abf000747aa1007a4a4200605064003f261a00786b730056423f004c271a0077463f0070494500b7bbca00755f5b00a9afd100635a6e00899bd5009698b3008c797600b0afb6007f4c4300654449003d231500988e9d00714c48006a382c0081473b00694744007b7d840070686a007070810076524d007d676e006c7384006a6061006e70760071433a0066362c00371e11006c585d004c312b00753d30007e443800633a3200726976007a7688005f484900855a540078524d005b4d53007f88a2006f656f007a4439006c392e00743c2e00786063007b616500733c30007e42350076423700683f37006c4a4700784d450082534c006c464000784d46006d5c650073423800743f3400783e32007f42340067595f008b808e00733d310084463800713c3100784238007b473d00804b410070433a00814e45007f4b42006b3d35007d443800773e32007b40330079403300807784008c83920064362c008d504200763e32007c4336007f463a008d504400744137008b5145007d453a007f4438008145370084483b00814639006b3e36007f7784007f76850067423d00773e3100723b2e007e4334007e423400703b2e007f443600783e3100804335007d433600854739007c4133006a464300726b77006f6674006c565b0067352700743b2c006c372a00743c2d00713a2c006d382a00783e2f00723a2d00783d2f00763d2f00773d2f007a3f300068555c00645c6900625a67007c7282005e342800683525006534250064332500623224006b3727006f392900683527006c3729006f392a0066342700673a30006f66750057505c0000000000000000000000000000000000000102030405060708090a0b0c0d0e010f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e2d3f404142434445464748494a4b124c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2c9d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafb0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff'

# create temp icon file
with tempfile.NamedTemporaryFile(delete=False) as iconFile:
	iconFile.write(binascii.unhexlify(ICON))
# call when closing application
def on_closing(iconfile):
	try:
		os.remove(iconfile.name)
	except Exception:
		pass
# register function to call when application is closing
atexit.register(lambda file=iconFile: on_closing(file))

class MyApp():
	fileList = {}
	
	def __init__(self):
		self.window = TK.Tk()
		self.window.iconbitmap(iconFile.name)
		self.window.title("ResourceTool")
		# get screen width and height
		screen_width = self.window.winfo_screenwidth()
		screen_height = self.window.winfo_screenheight()
		# calculate position x and y coordinates
		self.width = 400
		self.height = 460
		x = (screen_width/2) - (self.width/2)
		y = (screen_height/2) - (self.height/2)
		self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))
		self.window.resizable(width=False, height=False)
		self.SetUpGUI()

	def SetUpGUI(self):
		self.water = Label(self.window, text="Pream Pinbut")
		self.water.place(x=320, y=440)

		self.label1 = Label(self.window, text="Name")
		self.label1.grid(row=0, column=0)
		self.label2 = Label(self.window, text="Filepath")
		self.label2.grid(row=1, column=0)

		self.label3 = Label(self.window, text="Name")
		self.label3.grid(row=3, column=0)
		self.label4 = Label(self.window, text="Filepath")
		self.label4.grid(row=4, column=0)

		self.addName = Entry(self.window, width=40)
		self.addName.grid(row=0, column=1)
		self.addPath = Entry(self.window, width=40)
		self.addPath.grid(row=1, column=1)

		self.editName = Entry(self.window, width=46)
		self.editName.grid(row=3, column=1, columnspan=2)
		self.editPath = Entry(self.window, width=46)
		self.editPath.grid(row=4, column=1, columnspan=2)

		self.ButtonSelect = Button(self.window, text="...", command=self.SelectFile, width=4)
		self.ButtonSelect.grid(row=0, column=2, rowspan=2)
		self.ButtonAdd = Button(self.window, text="Add", command=self.Add, width=8)
		self.ButtonAdd.grid(row=0, column=3, rowspan=2)

		self.ButtonSelectEdit = Button(self.window, text="...", command=self.SelectFileEdit, width=8)
		self.ButtonSelectEdit.grid(row=3, column=3, rowspan=2)
		self.ButtonEdit = Button(self.window, text="Edit", command=self.Edit, width=50)
		self.ButtonEdit.grid(row=5, column=0, columnspan=4)
		self.ButtonDelete = Button(self.window, text="Delete", command=self.Delete, width=50)
		self.ButtonDelete.grid(row=6, column=0, columnspan=4)
		self.ButtonSave = Button(self.window, text="Save", command=self.Save, width=50)
		self.ButtonSave.grid(row=7, column=0, columnspan=4)
		self.ButtonLoad = Button(self.window, text="Load", command=self.Load, width=50)
		self.ButtonLoad.grid(row=8, column=0, columnspan=4)
		self.ButtonExport = Button(self.window, text="Export", command=self.Export, width=50)
		self.ButtonExport.grid(row=9, column=0, columnspan=4)

		self.tree = Treeview(self.window, columns=("Name", "Filepath"), show="headings")
		self.tree.column("Name", width=200)
		self.tree.heading("Name", text="Name")
		self.tree.column("Filepath", width=200)
		self.tree.heading("Filepath", text="Filepath")
		self.tree.grid(row=2, column=0, columnspan=4)
		self.tree.bind("<ButtonRelease-1>", self.OnSelectTree)

	def Start(self):
		self.window.mainloop()

	def Add(self):
		name = self.addName.get()
		filepath = self.addPath.get()
		if name == "" and filepath == "":
			return showinfo("ResourceTool", "Please enter a name and filepath")
		elif name == "":
			return showinfo("ResourceTool", "Please enter a name")
		elif filepath == "":
			return showinfo("ResourceTool", "Please enter a filepath")
		if name not in self.fileList:
			self.fileList[name] = filepath
			self.addName.delete(0, END)
			self.addPath.delete(0, END)
			return self.tree.insert("", "end", values=(name, filepath))

	def Edit(self):
		itemNumber = self.tree.focus()
		if itemNumber == "":
			return
		item = self.tree.item(itemNumber)
		newName = self.editName.get()
		newFilepath = self.editPath.get()
		if newName == "":
			return showinfo("ResourceTool", "Please enter a name")
		elif newFilepath == "":
			return showinfo("ResourceTool", "Please enter a filepath")
		elif newName in self.fileList and item["values"][0] != newName:
			return showinfo("ResourceTool", "Name already exists")
		elif newName not in self.fileList and item["values"][0] != newName:
			index = list(self.fileList.keys()).index(item["values"][0])
			self.fileList.pop(item["values"][0])
			items = list(self.fileList.items())
			items.insert(index, (newName, newFilepath))
			self.fileList = dict(items)
			
		self.tree.item(itemNumber, values=(newName, newFilepath))
	
	def Delete(self):
		itemNumber = self.tree.focus()
		if itemNumber == "":
			return
		item = self.tree.item(itemNumber)
		answer = askokcancel("ResourceTool", f"Are you sure you want to delete this item?\nName: {item['values'][0]}\nFilepath: {item['values'][1]}")
		if answer is False:
			return
		self.fileList.pop(item["values"][0])
		self.tree.delete(itemNumber)
		self.editName.delete(0, END)
		self.editPath.delete(0, END)

	def Save(self):
		filetypes = (
			("Resource Header Tool", "*.json"),
		)
		filepath = self.AskOpenFileName("save", filetypes)
		if filepath is None:
			return
		with open(filepath, "w") as f:
			json.dump(self.fileList, f)

	def Load(self):
		filetypes = (
			("Resource Header Tool", "*.json"),
		)
		filepath = self.AskOpenFileName("open", filetypes)
		if filepath is None:
			return
		with open(filepath, "r") as f:
			self.fileList = json.load(f)
			self.tree.delete(*self.tree.get_children())
			for name, filepath in self.fileList.items():
				self.tree.insert("", "end", values=(name, filepath))
	
	def Export(self):
		if not self.fileList:
			return showinfo("ResourceTool", "No files to export")
		outstr1 = hdata1
		outstr2 = cppdata1
		index = 0
		for name, filepath in self.fileList.items():
			# read file and convert data into hex
			outstr1 += f" {name}={index},"
			with open(filepath, "rb") as f:
				data = f.read()
				hexdata = binascii.hexlify(data).decode("utf-8")
				outstr2 += f"	{{ {name}, \"{hexdata}\" }},\n"
			index += 1
		#remove last comma
		outstr1 = outstr1[:-1]
		outstr1 += ";\n"
		outstr1 += hdata2
		outstr2 += cppdata2
		filepath = fd.askdirectory(
			title="ResourceTool",
			initialdir="./"
		)
		if filepath == "":
			return
		with open(f"{filepath}/Resource.h", "w") as f:
			f.write(outstr1)
		with open(f"{filepath}/Resource.cpp", "w") as f:
			f.write(outstr2)

	def OnSelectTree(self, event):
		itemNumber = self.tree.focus()
		if itemNumber == "":
			return
		item = self.tree.item(itemNumber)
		self.editName.delete(0, END)
		self.editName.insert(0, item["values"][0])
		self.editPath.delete(0, END)
		self.editPath.insert(0, item["values"][1])
	
	def SelectFileEdit(self):
		itemNumber = self.tree.focus()
		if itemNumber == "":
			return
		filetypes = (
			('All files', '*.*'),
		)
		filename = self.AskOpenFileName("open", filetypes)
		if filename is None:
			return
		self.editPath.delete(0, END)
		self.editPath.insert(0, filename)
	
	def SelectFile(self):
		filetypes = (
			('All files', '*.*'),
		)
		filename = self.AskOpenFileName("open", filetypes)
		if filename is None:
			return
		self.addPath.delete(0, END)
		self.addPath.insert(0, filename)
	
	def AskOpenFileName(self, type: str, filetypes):
		if type.lower() == "open":
			filename = fd.askopenfilename(
				title="Resource Header Tool",
				initialdir="./",
				filetypes=filetypes
			)
		elif type.lower() == "save":
			filename = fd.asksaveasfilename(
				title="Resource Header Tool",
				initialdir="./",
				filetypes=filetypes,
				defaultextension=".json"
			)

		if filename == "":
			return
		return filename

def main():
	app = MyApp()
	app.Start()

if __name__ == "__main__":
	main()
