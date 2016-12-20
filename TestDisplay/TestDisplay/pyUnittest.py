import sys

class pyUnitResults():

    def __init__(self):
        self.resultsLine

    def readResults(self, file):
        data = ""
        with open(file, 'r') as myfile:
            data=myfile.read()

        self.parseResults(data)
    # End readResults

    def parseResults(self, results):

        resultsSplit = results.split("\n")

        self.resultsLine = resultsSplit.pop(0)

        inFailedSection = False
        for line in split:
            if line.startswith("===="):
                inFailedSection = True

    # End parseResults

    def displayResultsLine(self):
        if self.resultsLine is not None:
            for i in range(0, len(self.resultsLine)):
                if self.resultsLine == '.':
                    self.outputSuccessBubble()
                else:
                    self.outputFailedBubble()
    # End displayResultsLine

    def writeHeader(self):
        print("<html><body>")
    # End writeHeader

    def writeFooter(self):
        print("</body></html>")
    # End writeFooter

    def display(self):
        self.writeHeader()
        self.displayResultsLine()
        self.writeFooter()
    # End display

# End pyUnitResults()

if __name__ == "__main__":
    dis = pyUnitResults()
    dis.readResults(sys.argv[1])
