#피처 선택(속성 선택)
#Select features
layer = iface.activeLayer()
layer.selectByExpression('"lbl_doub">1500', QgsVectorLayer.SetSelection)


##속성 선택 취소(피처 선택 취소)
#Remove selection
layer.removeSelection()