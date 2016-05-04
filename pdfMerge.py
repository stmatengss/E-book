from pyPdf import PdfFileWriter, PdfFileReader

output = PdfFileWriter()
input1 = PdfFileReader(file("static/output/1.0.pdf", "rb"))
input2 = PdfFileReader(file("static/output/1.1.pdf", "rb"))

output.addPage(input1.getPage(0))
output.addPage(input2.getPage(0))

outputStream = file("static/output/1.pdf", "wb")
output.write(outputStream)
outputStream.close()