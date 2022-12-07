

symbol = QgsFillSymbol.createSimple({'color': 'green'})
##layer.setOpacity(myOpacity)
layer.renderer().setSymbol(symbol)

# show the change
layer.triggerRepaint()