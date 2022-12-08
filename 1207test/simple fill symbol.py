

symbol = QgsFillSymbol.createSimple({'color': 'green'})
##layer.setOpacity(myOpacity) ..layer opacity
##symbol.setOpacity(myOpacity) ..symbol opacity
layer.renderer().setSymbol(symbol)

# show the change
layer.triggerRepaint()
