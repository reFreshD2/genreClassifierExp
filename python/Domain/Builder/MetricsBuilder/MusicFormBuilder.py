from Domain.Builder.IMusicMetricsBuilder import IMusicMetricsBuilder
import collections
import string


class MusicFormBuilder(IMusicMetricsBuilder):

    def __markFreq(self, freq):
        marks = {}
        markIndex = 0
        i = 0
        findingGroup = 0
        while i < len(freq) - 1:
            if marks.get(i) is not None:
                i += 1
                continue
            sameFreqIndex = self.__findSame(freq[i], freq[i+1:])
            marks[i] = markIndex
            if sameFreqIndex is not None:
                sameFreqIndex = i + 1 + sameFreqIndex
                findingGroup += 1
                j = i - 1
                prevMark = findingGroup - 1
                while j > 0 and marks[j] > prevMark:
                    marks[j] = prevMark
                    j -= 1
                marks[sameFreqIndex] = findingGroup
                marks[i] = findingGroup
                i += 1
                sameFreqIndex += 1
                while i < len(freq) and sameFreqIndex < len(freq) and freq[i] == freq[sameFreqIndex]:
                    marks[i] = findingGroup
                    marks[sameFreqIndex] = findingGroup
                    i += 1
                    sameFreqIndex += 1
                i -= 1
                markIndex = findingGroup
            markIndex += 1
            i += 1
        return marks

    def __findSame(self, finding, container):
        for i in range(0, len(container)):
            if finding == container[i]:
                return i
        return None

    def __getMark(self, index):
        return string.ascii_uppercase[index]

    def __isNotUsingMark(self, index, mark):
        while index >= 0:
            if string.ascii_uppercase[index] == mark:
                return False
            index -= 1
        return True

    def __mergeGroup(self, marks):
        mark = marks.get(0)
        for i in range(1, len(marks) - 1):
            if marks.get(i+1) - marks.get(i) == 1 or marks.get(i+1) - marks.get(i) == 0:
                marks[i] = mark
        return marks

    def __compressGroup(self, marks):
        result = {0: marks.get(0)}
        index = 1
        for i in range(1, len(marks)):
            if self.__findSame(marks.get(i), result) is None:
                result[index] = marks.get(i)
                index += 1
        return result

    def __mergeImpulse(self, marks):
        result = {}
        currentMark = 0
        isInc = True
        firstGroup = marks.get(0)
        for i in range(0, len(marks) - 1):
            if isInc and marks.get(i) < marks.get(i+1):
                isInc = False
            elif not isInc and marks.get(i) > marks.get(i+1):
                isInc = True
            else:
                result[currentMark] = firstGroup
                firstGroup = marks.get(i+1)
                currentMark += 1
        return result

    def __getForm(self, impulse):
        form = 'A'
        indexMark = 1
        for i in range(1, len(impulse) - 1):
            if impulse[i+1] - impulse[i] > 15:
                form += self.__getMark(indexMark)
                indexMark += 1
        return form

    def buildPart(self, metrics, freq, amp=None):
        markedFreq = self.__markFreq(freq)
        sortedMarks = collections.OrderedDict(sorted(markedFreq.items()))
        mergedFreq = self.__mergeGroup(sortedMarks)
        compressionFreq = self.__compressGroup(mergedFreq)
        impulse = self.__mergeImpulse(compressionFreq)
        newIter = self.__mergeImpulse(impulse)
        while len(impulse) - len(newIter) > 2:
            impulse = newIter
            newIter = self.__mergeImpulse(impulse)
        metrics.setForm(self.__getForm(impulse))
