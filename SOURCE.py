### AQUI METEMOS EL CODIGO DEL SOURCE ###
###############LIBRARIES###############
import CLASES as cl
import os
import datetime
import csv
import pandas as pd

#para usar el dia daytime.now() 
#print(f'{dateOfTOday.year}/{dateOfTOday.month}/{dateOfTOday.day}')

############## FUNCTIONS #############
def inventarioFileCheckUp():
    path = 'inventario.csv'
    check_file = os.path.isfile(path)
#print(check_file)

    if check_file:
        #print("FLAG")
        pass
    else:
        with open('inventario.csv', 'w', newline = '')as inventario:
            writer = csv.writer(inventario)
            writer.writerow(['NAME', 'ID', 'SKU', 'STOCK', 'PRESENTATION', 'LAB', 'COST', 'SALE', 'EXPDATE', 'IVA'])
            pass

def salesFileCheckUp():
    path ='salesDf.csv'
    check_file = os.path.isfile(path)
    if check_file:
        pass
    else:
        with open('salesDf.csv', 'w', newline = '') as salesDf:
            writer = csv.writer(salesDf)
            writer.writerow(['DATE', 'SALEID', 'ITEMS SOLD', 'PAYMENT TYPE', 'BILLING', 'SUBTOTAL', 'TOTAL'])
            pass

def soldItemsFileCheckUP():
    path = 'soldItems.csv'
    check_file = os.path.isfile(path)
    if check_file:
        pass
    else:
        with open('soldItems.csv', 'w', newline = '') as soldItems:
            writer = csv.writer(soldItems)
            writer.writerow(['ITEM', 'AMOUNT SOLD', 'SUBTOTAL', 'TOTAL'])

def csvObjectsTOItems(inventario, stablishment):
    for index in range (0, rowsQuant, 1):
        tempItem = cl.Item()
        tempItem.name = inventario['NAME'][index]
        tempItem.id = inventario['ID'][index]
        tempItem.sku = inventario['SKU'][index]
        tempItem.presentation = inventario['PRESENTATION'][index]
        tempItem.lab = inventario['LAB'][index]
        tempItem.stock = inventario['STOCK'][index] 
        tempItem.cost = inventario['COST'][index] 
        tempItem.sale = inventario['SALE'][index]  
        tempItem.expDate = inventario['EXPDATE'][index] 
        tempItem.iva = inventario['IVA'][index]
        stablishment.addItem(tempItem)
    
    return stablishment

def addingItemsToCSVsoldItems(stablishment):
    for index in range(0, len(stablishment.itemList), 1):
        with open('soldItems.csv', 'w') as soldItems:
            writer = csv.writer(soldItems)
            writer.writerow([stablishment.itemList[index].name, 0, 0, 0])
    return stablishment

def csvSalesToSaleObj(salesCSV, stablishment):
    for index in range (0, salesRowsQuant, 1):
        tempSale = cl.Sale()
        tempSale.saleId = salesCSV['SALEID'][index]
        tempSale.paymentType = salesCSV['PAYMENT TYPE'][index]
        tempSale.billing = salesCSV['BILLING'][index]
        tempSale.subtotal = salesCSV['SUBTOTAL'][index]
        tempSale.total = salesCSV['TOTAL'][index]
        #PARA EL ITEMS SOLD
        itemString = salesCSV['ITEMS SOLD'][index]
        tempSale.itemsSold = itemString.split(', ')
        #PARA LA FECHA
        tempSale.date = salesCSV['DATE'][index]
        stablishment.addSale(tempSale)
    return stablishment

def printMenu():
    print("--Welcome to Farmacias san Pablo--")
    print("Menu ")
    print("1. Add new item")
    print("2. Create a sale")
    print('3. Inventory management')
    print('4. Sales reports')
    print("5. Exit")

def addNewItem(stablishment):
    tempItem = cl.Item()
    tempItem.name = input("Introduce the name of the item: ")
    tempItem.sku = input("Introduce the SKU of the item: ")
    tempItem.id = itemID
    tempItem.presentation = input(f"Introduce the presentation of {tempItem.name}: ")
    tempItem.lab = input("Introduce the laboratory: ")
    tempItem.stock = int(input("Introduce the stock of the item: "))
    tempItem.cost = float(input("Introduce the cost value of the item: $"))
    tempItem.sale = float(input("Introduce the sale value of the item: $"))
    print("Introduce the expiration date")
    y = int(input("Introduce the year: "))
    m = int(input("introduce the month: "))
    d = int(input("Introduce the day: "))
    tempItem.expDate = (y, m, d)
    tempIVA = input("Does the object have iva? y/n: ")
    tempItem.iva = ivaValidation(tempIVA)
    stablishment.addItem(tempItem)
    return stablishment

def ivaValidation(tempIVA):
    flag = True
    if tempIVA == "y":
        pass
    elif tempIVA == "n":
        flag = False
    return flag

def addItem(stablishment):
    #
    #stablishment.showInventory()
    tempItem = cl.Item()
    tempItem.name = input("Introduce the name of the item: ")
    #
    #tablishment.showInventory()
    flag = stablishment.validItem(tempItem)
    #print(f"flag {flag}")
    if flag == True:        
        print("The item is already on the system")
        opt = input("Type any key to return to the main menu: ")
    else:
        tempItem.sku = input("Introduce the SKU of the item: ")
        tempItem.id = itemID
        tempItem.presentation = input(f"Introduce the presentation of {tempItem.name}: ")
        tempItem.lab = input("Introduce the laboratory: ")
        tempItem.stock = int(input("Introduce the stock of the item: "))
        tempItem.cost = float(input("Introduce the cost value of the item: $"))
        tempItem.sale = float(input("Introduce the sale value of the item: $")) 
        y = int(input("Introduce the year: "))
        m = int(input("introduce the month: "))
        d = int(input("Introduce the day: "))
        tempItem.expDate = (y, m, d)
        tempIVA = input("Does the object have iva? y/n: ")
        tempItem.iva = ivaValidation(tempIVA)
        stablishment.addItem(tempItem)
        stablishment.addItemToDf(tempItem)
        stablishment.addItemToItemSoldDF(tempItem)

        
    return stablishment

def createSale(stablishment, saleCont):
    dateOfTOday = datetime.date.today()
    buyMenuRunControl = True
    tempSale = cl.Sale()
    tempSale.saleId = saleCont
    tempSale.date = (f'{dateOfTOday.year, dateOfTOday.month, dateOfTOday.day}')
    
    
    while buyMenuRunControl:
        tempItem = cl.SoldItem()
        print("Item list")
        stablishment.showInventory()
        tempSale.buyItem(stablishment, tempItem)
        runControl = input("Do you want to add another product? y/n: ")
        if runControl == "n":
            tempSale.paymentType = input("Please introduce the payment type (card/cash): ")
            tempPaymentType = input("The sale will be billed y/n? ")
            if tempPaymentType == 'n':
                tempSale.billing = False
            elif tempPaymentType == 'y':
                tempSale.billing == True
                
            tempSale.creatingTotal()
            buyMenuRunControl = False
            stablishment.addSale(tempSale)
            stablishment.addSaleToDf(tempSale)

            
       
            opt = input("Press enter to continue: ")
        elif runControl == "y":
            pass

    return stablishment

def inventoryManagementSubMenu():
    print("Inventory management")
    print('1. Search by name')
    print('2, Search by SKU')
    print('3. Search by laboratory')
    print('4. Check the stock of any product')
    print('5. Check the expiration date')

def salesReportSubMenu():
    print('Sales reports')
    print('1. Sales information by ID')
    print('2. Daily reports')
    print('3. Weekly reports')
    print('4. Yearly reports')
    print('5. Sold products')
    print('6. Payment type sales reports')
    print('')

def searchByName(stablishment):
    os.system('cls')
    inventario = pd.read_csv('inventario.csv')
    print("Item search by name")
    print("-------------------")
    print('Item list')
    print('')
    for i in range (0, len(stablishment.itemList), 1):
        print(f'{i+1}. {stablishment.itemList[i].name}')
        print('')
    rowCont = 0
    item = input("Introduce the name of the item: ")
    for i in range (0, len(stablishment.itemList), 1):
        rowCont+=1
        if stablishment.itemList[i].name == item:
            break
    print(inventario.loc[[rowCont-1]])
    
    print("")
    opt = input("Press enter to return to the main menu: ")
    
    return stablishment

def searchBySku(stablishment):
    os.system('cls')
    inventario = pd.read_csv('inventario.csv')
    print("Item search by SKU")
    print("-------------------")
    print('Items SKU list')
    print('')
    for i in range (0, len(stablishment.itemList), 1):
        print(f'{i+1}. {stablishment.itemList[i].sku}')
        print('')
    rowCont = 0
    item = input("Introduce the SKU of the item: ")
    for i in range (0, len(stablishment.itemList), 1):
        rowCont+=1
        if stablishment.itemList[i].sku == item:
            break
    print(inventario.loc[[rowCont-1]])
    
    print("")
    opt = input("Press enter to return to the main menu: ")
    
    return stablishment

def searchByLab(stablishment):
    os.system('cls')
    inventario = pd.read_csv('inventario.csv')
    print("Item search by laboratory")
    print("-------------------")
    print('Items laboratory list')
    print('')
    
    emptyList = []
    for index in range (0, len(stablishment.itemList), 1):
        emptyList.append(stablishment.itemList[index].lab)
        
    labSet = set(emptyList)
    
    print(labSet)
    print('')
    item = input("Introduce the laboratory: ")

    print(inventario[(inventario['LAB'] == item)])
    print("")
    opt = input("Press enter to return to the main menu: ")
    
    return stablishment

def checkStock(stablishment):
    os.system('cls')
    inventario = pd.read_csv('inventario.csv')
    print('Stock management')
    print('-----------------')
    print('')
    print('Item list')
    print('')
    for i in range (0, len(stablishment.itemList), 1):
        print(f'{i+1}. {stablishment.itemList[i].name}')
        print('')
    
    item = input('Input the name of the item you want to check: ')
    rowCont = 0
    
    for i in range (0, len(stablishment.itemList), 1):
        rowCont+=1
        if stablishment.itemList[i].name == item:
            break
    print(f'Stock of {item}:')
    print(inventario['STOCK'][rowCont])
    
    print("")
    opt = input("Press enter to return to the main menu: ")

def checkExpDate(stablishment):
    os.system('cls')
    inventario = pd.read_csv('inventario.csv')
    print("Expiration dates management")
    print("-------------------")
    print('Item list')
    print('')
    for i in range (0, len(stablishment.itemList), 1):
        print(f'{i+1}. {stablishment.itemList[i].name}')
        print('')
    rowCont = 0
    item = input("Introduce the name of the item: ")
    for i in range (0, len(stablishment.itemList), 1):
        rowCont+=1
        if stablishment.itemList[i].name == item:
            break
    expDate = inventario['EXPDATE'][rowCont]
    print(f'Expiration date of {item}: {expDate}')
    
    print("")
    opt = input("Press enter to return to the main menu: ")
    
    return stablishment
    
def salesIdReport(stablishment):
    salesCSV = pd.read_csv('salesDF.csv')
    os.system('cls')
    print('Sales information by ID')
    print('')
    for index in range(0, len(stablishment.salesList), 1):
        print(f'ID: {stablishment.salesList[index].saleId} Date: {stablishment.salesList[index].date}')
    
    item = int(input('Select the ID: '))
    rowCont = 0

    for i in range (0, len(stablishment.salesList), 1):
        rowCont+=1
        if stablishment.salesList[i].saleId == item:
            break
    print(salesCSV.loc[[rowCont-1]])
    opt = input("Press enter to return to the main menu: ")

def dailyReports(stablishment, dateOfTOday):
    salesCSV = pd.read_csv('salesDF.csv')
    os.system('cls')
    todayDate = str(dateOfTOday)
    cellCont = 0
    for index in range(0, len(stablishment.salesList), 1):
        scvDate = str(salesCSV['DATE'][index])
        if  todayDate == scvDate:
            print(salesCSV.loc[[index]])
        cellCont += 1
    opt = input("Press enter to return to the main menu: ")
    
def yearReports(stablishment):
    print("YEARLY SALES REPORT")
    print('')
    salesCSV = pd.read_csv('salesDF.csv')
    os.system('cls')
    yearToday = datetime.datetime.now()
    todayDate = str('('+ f'{yearToday.year}')
    
    cellCont = 0
    for index in range(0, len(stablishment.salesList), 1):
        csvDate = str(salesCSV['DATE'][index])
        tempList = csvDate.split(', ')

        if  todayDate == tempList[0]:
            print(salesCSV.loc[[index]])
        cellCont += 1
    opt = input("Press enter to return to the main menu: ")
    
def soldProdReport(stablishment):
    os.system('cls')
    soldItemsCSV = pd.read_csv('soldItems.csv')
    print('Sold products reports')
    print('')
    print()
    print('Item list')
    print('')
    for i in range (0, len(stablishment.itemList), 1):
        print(f'{i}. {stablishment.itemList[i].name}')
        print('')
    
    item = int(input("Select the ID of the item: "))
    saleVolume = soldItemsCSV['TOTAL'][item] 
    
    profit = (stablishment.itemList[item].sale - stablishment.itemList[item].cost) * int(soldItemsCSV['AMOUNT SOLD'][item])
    print(f'Data from {stablishment.itemList[item].name}')
    print(f'Item: {stablishment.itemList[item].name}   Sales volume: ${saleVolume}   Profit: ${profit}')
    
    
    print('')
    opt = input("Press enter to return to the main menu: ")
    pass

def paymentSaleReport(stablishment):
    salesCSV = pd.read_csv('salesDF.csv')
    os.system('cls')
    miniMenuControl = True
    print('Payment type reports')
    print('')
    print('1. Card')
    print('2. Cash')
    select = int(input("Select an option: "))
    if select == 1:
        print(salesCSV.loc[salesCSV['PAYMENT TYPE'] == 'card'])
        
    elif select == 2:
        print(salesCSV.loc[salesCSV['PAYMENT TYPE'] == 'cash'])

    opt = input("Press enter to return to the main menu: ")

############### VARIABLES ##################
inventarioFileCheckUp()
salesFileCheckUp()
soldItemsFileCheckUP()
SanPablo1st = cl.Establishment("San Pablo first establishment")
inventario = pd.read_csv('inventario.csv')


salesCSV = pd.read_csv('salesDF.csv')
soldItemsCSV = pd.read_csv('soldItems.csv')

menuOption = 0
programRunning = True
rowsQuant = inventario.shape[0]
salesRowsQuant = salesCSV.shape[0]
itemID = 0 + rowsQuant
saleCont = 0 + salesRowsQuant
dateOfTOday = datetime.date.today()
dateOfTOday = (dateOfTOday.year, dateOfTOday.month, dateOfTOday.day)
print(dateOfTOday)
#PASAREMOS LOS DATOS DE NUESTRO CSV A OBJETOS DE TIPO ITEM


SanPablo1st = csvObjectsTOItems(inventario, SanPablo1st)
SanPablo1st = csvSalesToSaleObj(salesCSV, SanPablo1st)
#SanPablo1st = addingItemsToCSVsoldItems(SanPablo1st)
################## MAIN ###############################

while programRunning:
    os.system('cls')
    printMenu()
    menuOption = int(input("Select an option: "))
    if menuOption == 1:
        os.system('cls')    
        SanPablo1st = addItem(SanPablo1st) 
        itemID += 1
    
    if menuOption == 2:
        os.system('cls')
        SanPablo1st = createSale(SanPablo1st, saleCont)
        saleCont += 1
    
    if menuOption == 3:
        os.system('cls')
        inventoryManagementSubMenu()
        subMenuOption = int(input('Select an option: '))
        if subMenuOption == 1:
            SanPablo1st = searchByName(SanPablo1st)
        
        if subMenuOption == 2:
            SanPablo1st = searchBySku(SanPablo1st)
            pass
        
        if subMenuOption == 3:
            SanPablo1st = searchByLab(SanPablo1st)
        
        if subMenuOption == 4:
            SanPablo1st = checkStock(SanPablo1st)
        
        if subMenuOption == 5:
            SanPablo1st = checkExpDate(SanPablo1st)
        pass
    
    if menuOption == 4:
        os.system('cls')
        salesReportSubMenu()
        subMenuOption = int(input("Select an option: "))
        if subMenuOption == 1:
            os.system('cls')
            salesIdReport(SanPablo1st)
            pass
        
        if subMenuOption == 2:
            os.system('cls')
            dailyReports(SanPablo1st, dateOfTOday)
            pass
        
        if subMenuOption == 3:
            os.system('cls')

            pass
        
        if subMenuOption == 4:
            os.system('cls')
            yearReports(SanPablo1st)
            pass
        #####################################
        if subMenuOption == 5:
            os.system('cls')
            soldProdReport(SanPablo1st)
            pass
        
        if subMenuOption == 6:
            os.system('cls')
            paymentSaleReport(SanPablo1st)
            pass
        
    if menuOption == 5:
        
        programRunning = False

        
        
        

        