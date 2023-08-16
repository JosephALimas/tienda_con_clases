import datetime
import pandas as pd
import csv

class Item:
    def __init__(self, name = "" ,id = 0, stock = 0, cost = 0.0, sale = 0.0, expDate = datetime.date(2023, 12, 1), lab = "", presentation = "", iva = True, sku = "" ):
        self.name = name 
        self.id = id
        self.sku = sku
        self.presentation = presentation
        self.lab = lab
        self.stock = stock
        self.cost = cost
        self.sale = sale
        self.expDate = expDate
        self.iva = iva
    def printItemData(self):
        print(f"Item: {self.name} ---- ID: {self.id} ---- SKU: {self.sku} ---- Expiration date: {self.expDate}")
        print(f"Stock: {self.stock} ---- Laboratory: {self.lab} ---- Presentation: {self.presentation}")
        print(f"Cost value: {self.cost} ---- Sale value: {self.sale} ---- Iva: {self.iva}")

class Establishment:
    def __init__(self, sn = ""):
        self.sn = sn
        self.itemList = []
        self.salesList = []
    def addItem(self, item):
        self.itemList.append(item)
        
        #print(self.itemList[0].name)
    def addItemToDf(self, item):
        with open('inventario.csv', 'a', newline = '') as inventario_csv:
            writer = csv.writer(inventario_csv)
            nueva_fila = [item.name, item.id, item.sku, item.stock, item.presentation, item.lab, item.cost, item.sale, item.expDate, item.iva]
            writer.writerow(nueva_fila)

    def showInventory(self):
        for i in range (0, len(self.itemList), 1):
            print(f"{self.itemList[i].id}: {self.itemList[i].name}   Stock: {self.itemList[i].stock}")
            
            print()

    def ShowSpecificItemData(self, ID = ""):
        for item in self.itemList:
            if item.id == ID:
                item.printItemData()
                break
            else:
                ("ID not found")
    #nos va a ayudar a checar si el objeto no fue introducido antes con otra presentacion
    def validItem(self, tempItem = ""):
        flag = False
        #print(self.itemList[0].name)
        for index in range  (0, len(self.itemList), 1):
            if self.itemList[index].name == tempItem.name:
                flag = True
            elif self.itemList[index].name != tempItem.name:
                pass
        
        return flag
    
    def addSale(self, sale):
        self.salesList.append(sale)
    def addSaleToDf(self, sale):
        #CODIGO PARA CREAR UN STRING CON LA LISTA DE ITEMS COMPRADOS
        itemsList = ', '.join(sale.itemNamesSold)
        
        with open('salesDf.csv', 'a', newline = '') as salesDf:
            writer = csv.writer(salesDf)
            nueva_fila = [sale.date, sale.saleId, itemsList, sale.paymentType, sale.billing, sale.subtotal, sale.total]
            writer.writerow(nueva_fila)
    def addItemToItemSoldDF(self, item):
        with open('soldItems.csv', 'a', newline = '') as soldItems:
            writer = csv.writer(soldItems)
            nueva_fila = [item.name, 0, 0, 0]
            writer.writerow(nueva_fila)        
        
class SoldItem(Item):
    def __init__(self, itemName = "", amountSold = 0, subtotal = 0.0, total = 0.0):
        #self.itemName = itemName
        self.amountSold = amountSold
        self.subtotal = subtotal
        self.total = total
           
class Sale:
    
    def __init__(self, date = [], saleId = 0, subtotal = 0.0, total = 0.0, paymentType = "", billing = True):
        self.date = date
        self.saleId = saleId
        self.subtotal = subtotal
        self.total = total
        self.paymentType = paymentType
        self.billing = billing
        self.itemsSold = []
        #
        self.itemNamesSold = []
    def buyItem(self, stablishment, item):
        itemSelect = int(input("Select the ID of the item you want to buy: "))
        itemFInderControl = False
        #for updating the row on the csv
        rowUpdater = 0
        while itemFInderControl == False:
            
            for index in range (0, len(stablishment.itemList), 1):
                
                if itemSelect  == stablishment.itemList[index].id:
                    item.name = stablishment.itemList[index].name
                    item.sku = stablishment.itemList[index].sku
                    item.id = stablishment.itemList[index].id
                    item.presentation = stablishment.itemList[index].presentation
                    item.lab = stablishment.itemList[index].lab
                    item.stock = stablishment.itemList[index].stock
                    item.cost = stablishment.itemList[index].cost
                    item.sale = stablishment.itemList[index].sale
                    item.expDate = stablishment.itemList[index].expDate
                    item.iva = stablishment.itemList[index].iva

                    item.amountSold = int(input(f"How many {item.name} do you want to buy? "))
                    stablishment.itemList[index].stock = stablishment.itemList[index].stock - item.amountSold
                    item.subtotal = (item.cost*item.amountSold)
                    if item.iva == True:      
                        item.total = (item.subtotal + (item.subtotal * 0.16))
                    elif item.iva == False:
                        item.total = item.subtotal
                    itemFInderControl = True
                    self.itemsSold.append(item) 
                    self.itemNamesSold.append(item.name)
                    rowUpdater	= index
                else:
                    pass 
            
            
            
            if itemFInderControl == True:
                break
            elif itemFInderControl == False:
                print("Error finding the item, please try again")
                opt = input("Press any key to return to the menu: ")
                break
            
        #ACTUALIZAMOS EL CSV CON EL NUEVO STOCK DEL PRODUCTO DESPUES DE LA COMPRA
        myList = []
        with open('inventario.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = stablishment.itemList[rowUpdater].stock
        myList[rowUpdater+1][3] = newDetail

        with open('inventario.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)

        #ACTUALIZAMOS EL SOLDITEMS.CSV CON LOS DATOS NUEVOS DE COMPRA DE CADA OBJETO
        #MODIFICAMOS EL AMOUNT SOLD
        
        list2 = []
        with open('soldItems.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    list2.append(row)
  
        oldValue = int(list2[rowUpdater+1][1])
        newDetail = item.amountSold + oldValue
        list2[rowUpdater+1][1] = newDetail

        with open('soldItems.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in list2:
                if row: 
                    myFile.writerow(row)

        #MODIFICAMOS EL SUBTOTAL
        list3 = []
        with open('soldItems.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    list3.append(row)
  
        oldValue = float(list2[rowUpdater+1][2])
        newDetail = item.subtotal + oldValue
        list3[rowUpdater+1][2] = newDetail

        with open('soldItems.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in list3:
                if row: 
                    myFile.writerow(row)

        #MODIFICAMOS EL TOTAL
        list4 = []
        with open('soldItems.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    list4.append(row)
        print(f'TOTAL {item.total}')
        oldValue = float(list4[rowUpdater+1][3])
        newDetail = item.total + oldValue
        list4[rowUpdater+1][3] = newDetail

        with open('soldItems.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in list4:
                if row: 
                    myFile.writerow(row)

    def creatingTotal(self):
        for index in range(0, len(self.itemsSold), 1):
            self.subtotal = self.subtotal + self.itemsSold[index].subtotal
            self.total = (self.itemsSold[index].total) + self.total
        #print(self.itemsSold[0].iva)
        print("////////////////////////////")
        print('')
        print(f"Subtotal: {self.subtotal}")
        print('')
        print(f"Total: {self.total}")
        print('')
     
