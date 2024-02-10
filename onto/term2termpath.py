class Term2TermPath:
    ancestor = None
    leftBranch = []
    rightBranch = []
    fullPath = []

    leftHash = None
    rightHash = None

    def __init__(self, ancestor, currentBranch, branch):
        self.leftBranch = []
        self.rightBranch = []
        self.fullPath = []

        self.ancestor = ancestor

        self.leftBranch.extend(currentBranch)
        self.leftHash = self.do_hash(currentBranch)

        self.rightBranch.extend(branch)
        self.rightHash = self.do_hash(branch)

        self.fullPath.extend(self.leftBranch)
        self.fullPath.extend(self.rightBranch)

    def do_hash(self, path):
        sHash = ''
        if not path:
            return sHash

        for s in path:
            sHash += s + '-'

        return sHash[0: len(sHash) - 1]

    def hasBranches(self, leftBranch, rightBranch):
        return (self.leftHash == leftBranch and self.rightHash == rightBranch) or (
                    self.leftHash == rightBranch and self.rightHash == leftBranch)

    def getFullPath(self):
        return self.fullPath
