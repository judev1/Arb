class Arb:

    PRECISION = 3

    def __init__(self, num):

        self.digits = list()

        num = str(num)

        if "e" in num:

            # In the case that the number provided contains a whole integer
            # exponent, we calculate its true value
            man, e = map(Arb, num.split("e"))
            for i in range(int(e)):
                if e.sign == 1:
                    man *= Arb(10)

            self.digits = man.digits
            self.dp = man.dp
            self.sign = man.sign

        else:

            # Creates a temporary value
            temp = num

            if "." in temp:
                temp = temp.replace(".", "", 1)
            if temp[0] == "-":
                temp = temp[1:]
            elif temp[0] == "+":
                temp = temp[1:]

            # Raises an exception if the number contains non numeric characters
            if not temp.isnumeric():
                raise Exception(f"'{num}' cannot be interpreted as a number")

            # Checks if the number string starts with +/- and determines the
            # sign
            if num[0] == "-":
                num = num[1:]
                self.sign = -1
            elif num[0] == "+":
                num = num[1:]
                self.sign = 1
            else:
                self.sign = 1

            # As a default the decimal point is set to the number of digits,
            # where the first decimal point would be in the case the number is
            # an integer
            self.dp = len(num.replace(".", ""))

            # Locate the decimal point
            for i, digit in enumerate(num):
                if digit == ".":
                    self.dp = i
                else:
                    self.digits.append(int(digit))

            # For numbers provided that start with a decimal point
            if self.dp == 0:
                self.dp = 1
                self.digits.insert(0, 0)

    @staticmethod
    def new(digits, dp, sign=1):
        arb = Arb(0)
        arb.digits = digits.copy()
        arb.dp = dp
        arb.sign = sign
        return arb

    def __copy__(self):
        arb = Arb(0)
        arb.digits = self.digits.copy()
        arb.dp = self.dp
        arb.sign = self.sign

    def __round__(self, precision):

        # Checks if self has any decimal places to round
        if self.dp == len(self.digits):
            return self.digits.copy(), self.dp

        # Sets the index to start from the last relevant decimal point
        index = self.dp + precision - 1

        # Splits the list to include only the relevant decimals
        digits = self.digits[:index+1]

        # Checks if there is an additional decimal
        if len(self.digits) > index+1:
            # Checks if the decimal is great enough to round up the last digit
            if self.digits[index+1] >= 5:
                # While the last digit is 9, remove it (rounds to 0)
                while digits[index] == 9:
                    # Remove the digit if it is before the decimal point
                    if index < self.dp:
                        digits[index] = 0
                    else:
                        digits.pop()
                    # Shift the focus onto the new last digit since there will
                    # be a carry which will round up the new last digit
                    index -= 1
                    # If the index exhausts all digits, the first digit will be
                    # 1
                    if index == -1:
                        digits.insert(0, 1)
                        return digits, len(digits)
                # Round up the last decimal
                digits[index] += 1

        # Removes trailing zero decimals
        while len(digits) > self.dp and digits[-1] == 0:
            digits.pop()

        return digits, self.dp

    def __str__(self):
        string = "-" if self.sign == -1 else ""
        digits, dp = self.__round__(Arb.PRECISION)
        for i, digit in enumerate(digits):
            if i == dp:
                string += "."
            string += str(digit)
        return string

    def __float__(self):
        return float(self.__str__())

    def __int__(self):
        return int(self.__str__())

    @staticmethod
    def __trueeq__(digits1, dp1, sign1, digits2, dp2, sign2):

        # Checks if an arb has a different sign
        if sign1 != sign2:
            return False

        # Checks if an arb has have more integer places
        if dp1 != dp2:
            return False

        # Iterates through the digits of arb1 and arb2. They can be zipped
        # since they will always be the same size
        for digit1, digit2 in zip(digits1, digits2):
            # Checks if values are not equal
            if digit1 != digit2:
                return False

        # Values must be equal
        return True

    @staticmethod
    def __truelt__(digits1, dp1, sign1, digits2, dp2, sign2):

        # Checks if an arb has a different sign
        if sign1 != sign2:
            return sign1 < sign2

        # Checks if an arb has have more integer places
        if dp1 != dp2:
            return dp1 < dp2

        # Iterates through the digits of arb1 and arb2. They can be zipped
        # since they will always be the same size
        for digit1, digit2 in zip(digits1, digits2):
            # If values are not equal then one is smaller
            if digit1 != digit2:
                return digit1 < digit2

        # Values must be equal
        return False

    def __eq__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform comparison on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        return Arb.__trueeq__(digits1, dp1, sign1, digits2, dp2, sign2)

    def __neq__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform comparison on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        return not Arb.__trueeq__(digits1, dp1, sign1, digits2, dp2, sign2)

    def __lt__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform comparison on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        return Arb.__truelt__(digits1, dp1, sign1, digits2, dp2, sign2)

    def __gt__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform comparison on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        return (
            not Arb.__truelt__(digits1, dp1, sign1, digits2, dp2, sign2) and
            not Arb.__trueeq__(digits1, dp1, sign1, digits2, dp2, sign2)
        )

    def __lte__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform comparison on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        return (
            Arb.__truelt__(digits1, dp1, sign1, digits2, dp2, sign2) or
            Arb.__trueeq__(digits1, dp1, sign1, digits2, dp2, sign2)
        )

    def __gte__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform comparison on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        return (
            not Arb.__truelt__(digits1, dp1, sign1, digits2, dp2, sign2) or
            Arb.__trueeq__(digits1, dp1, sign1, digits2, dp2, sign2)
        )

    @staticmethod
    def __trueadd__(digits1, dp1, digits2, dp2):

        # Defines the initial carry to be 0 and the digits to be decimals that
        # arb1 (self) may have in excess of arb2
        carry = 0
        digits = digits1[dp1 + len(digits2) - dp2: dp1 + Arb.PRECISION]

        # Defines the length to be the arbitrary precision or the length of
        # arb2 if it does not have enough decimals
        length = min(len(digits2), dp2 + Arb.PRECISION)

        # Iterates through the indexes of arb2
        for i in range(length - 1, -1, -1):
            # Checks if arb1 has FEWER INTEGER places than the current index of
            #       OR
            # Checks if arb1 has FEWER DECIMAL places than the current index of
            # arb2
            # So that arb1's value can be set to 0
            if dp1 < dp2 - i or len(digits1) - dp1 < i - dp2 + 1:
                value1 = 0
            else:
                value1 = digits1[dp1 + i - dp2]
            # Calculates the new value as well as the carry
            newvalue = (value1 + digits2[i] + carry) % 10
            carry = (value1 + digits2[i] + carry) // 10
            # Inserts the value into the beginning of the list
            digits.insert(0, newvalue)

        # Checks if arb1 has MORE INTEGER places than arb2
        if dp1 > dp2:
            # Sets the new arb's dp to be equal to arb1's
            dp = dp1
            # Inserts the excess integers from arb1 into the beginning of the
            # list
            digits.insert(0, *digits1[:dp1 - dp2])
            # Continues to round up the next value while there is a carry
            i = 1
            while carry:
                # Checks if there is an overflow or another digit to increment
                if dp1 - dp2 - i < 0:
                    # Moves the decimal point down 1 and inserts the carry
                    # into the beginning of the list
                    dp += 1
                    digits.insert(0, 1)
                else:
                    # Increments the digit and calculates if there is a carry
                    digits[dp1 - dp2 - i] = (digits[dp1 - dp2 - i] + 1) % 10
                    carry = (digits[dp1 - dp2 - i] + 1) // 10
                    i += 1
        else:
            # Sets the new arb's dp to be equal to arb2's
            dp = dp2
            # If there is a carry there must be an overflow
            if carry:
                # Moves the decimal point down 1 and inserts the carry
                # into the beginning of the list
                dp += 1
                digits.insert(0, 1)

        return digits, dp

    @staticmethod
    def __truesub__(digits1, dp1, digits2, dp2):

        # Defines the initial carry to be 0 and the digits to be decimals that
        # arb1 may have in excess of arb2
        carry = 0
        digits = digits1[dp1 + len(digits2) - dp2: dp1 + Arb.PRECISION]

        # Defines the length to be the arbitrary precision or the length of
        # arb2 if it does not have enough decimals
        length = min(len(digits2), dp2 + Arb.PRECISION)

        # Iterates through the indexes of arb2
        for i in range(length - 1, -1, -1):
            # Checks if arb1 has FEWER DECIMAL places than the current index of
            # arb2. NOTE: arb1 should never have fewer integer places
            # So that arb1's value can be set to 0
            if len(digits1) - dp1 < i - dp2 + 1:
                newvalue = (10 - digits2[i] + carry) % 10
                carry = -1
            else:
                value1 = digits1[dp1 + i - dp2]
                newvalue = (value1 - digits2[i] + carry) % 10
                carry = (value1 - digits2[i] + carry) // 10
            # Inserts the value into the beginning of the list
            digits.insert(0, newvalue)

        # Checks if arb1 has MORE INTEGER places than arb2
        if dp1 > dp2:
            # Sets the new arb's dp to be equal to arb1's
            dp = dp1
            # Inserts the excess integers from arb1 into the beginning of the
            # list
            digits.insert(0, *digits1[:dp1 - dp2])
            # Continues to round up the next value while there is a carry
            i = 1
            while carry:
                # Increments the digit and calculates if there is a carry
                value1 = digits[dp1 - dp2 - i]
                digits[dp1 - dp2 - i] = (value1 - 1) % 10
                carry = (value1 - 1) // 10
                i += 1
        else:
            # Sets the new arb's dp to be equal to arb2's (and arb1's)
            dp = dp2
            # If there is a carry there must be an overflow
            if carry:
                # Moves the decimal point down 1 and inserts the carry
                # into the beginning of the list
                dp += 1
                digits.insert(0, 1)

        # Removes leading zeros and moves the decimal place forwards
        while digits[0] == 0 and dp > 1:
            dp -= 1
            digits.pop(0)

        return digits, dp

    @staticmethod
    def __truemul__(digits1, dp1, digits2, dp2):

        dp = 0
        digits = [0]

        # print(digits1, dp1, digits2, dp2)


        # Iterates through every digit in arb1 to be multiplied by each digit
        # in arb2
        for i, value1 in enumerate(digits1):
            for j, value2 in enumerate(digits2):
                # print(i, j, digits)

                # Calculates the displacement of the digit from the ones column
                displacement1 = (i - dp1 if i - 1 < dp1 else i - dp1) + 1
                displacement2 = (j - dp2 if j - 1 < dp2 else j - dp2) + 1

                # Uses the displacements to work out the new value's
                # displacement and then its index
                displacement = displacement1 + displacement2
                index = dp + displacement

                # Checks if the index exists in the digits list and extends the
                # list if it doesn't
                while index < 0:
                    digits.insert(0, 0)
                    index += 1
                    dp += 1
                while index >= len(digits):
                    digits.append(0)

                # print(index, dp, displacement1, displacement2)

                value = (value1 * value2 + digits[index]) % 10
                carry = (value1 * value2 + digits[index]) // 10

                # print("In", index - dp, f"column ({index})")
                # print(f" :: {value1}*{value2} + {digits[index]} -> {carry}, {value}")

                digits[index] = value
                # print(" ::", digits, index, displacement, dp)

                while carry:

                    displacement -= 1
                    index -= 1

                    # Checks if the index exists in the digits list and extends the
                    # list if it doesn't
                    while index < 0:
                        index += 1
                        dp += 1
                        digits.insert(0, 0)

                    oldcarry = carry

                    value = (carry + digits[index]) % 10
                    carry = (carry + digits[index]) // 10

                    # print(" :: In", index - dp, f"column ({index})")
                    # print(f" :: :: {oldcarry} + {digits[index]} -> {carry}, {value}")

                    digits[index] = value
                    # print(" :: ::", digits, dp)

        #         input()
        # print(digits, dp)

        # Remove leading zeros
        while digits[0] == 0 and dp > 0:
            digits.pop(0)
            dp -= 1

        return digits, dp + 1

    def __add__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform addition on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        # Checks if the signs of the Arb objects are the same
        if sign1 == sign2:
            # In addition, when the signs are the same, the sign of the result
            # will be the same as signs of the Arb objects and since the Arb
            # objects have the same sign, either can be used.
            sign = sign1
            digits, dp = Arb.__trueadd__(digits1, dp1, digits2, dp2)
        else:
            # Checks if the absolute value of arb1 is smaller than arb2 so that
            # the order which they are subtracted in and their signs are switch
            # to make subtraction easier
            if Arb.__truelt__(digits1, dp1, 1, digits2, dp2, 1):
                arb0, digits0, dp0 = arb1, digits1, dp1
                arb1, digits1, dp1 = arb2, digits2, dp2
                arb2, digits2, dp2 = arb0, digits0, dp0
                # The sign will be that of the number being subtracted, but
                # since the numbers were switched its what used to be arb1
                sign = sign2
            else:
                # The sign will be that of the number being subtracted
                sign = sign1
            digits, dp = Arb.__truesub__(digits1, dp1, digits2, dp2)

        return Arb.new(digits, dp, sign)

    def __sub__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform subtraction on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        # Get the signs for the Arb object
        sign1, sign2 = arb1.sign, arb2.sign

        # Checks if the signs of the Arb objects are the same
        if sign1 == sign2:
            # Checks if the absolute value of arb1 is smaller than arb2 so that
            # the order which they are subtracted in and their signs are switch
            # to make subtraction easier
            if Arb.__truelt__(digits1, dp1, 1, digits2, dp2, 1):
                arb0, digits0, dp0 = arb1, digits1, dp1
                arb1, digits1, dp1 = arb2, digits2, dp2
                arb2, digits2, dp2 = arb0, digits0, dp0
                # Since the Arb objects have the same sign, either can be used.
                # The answer will have the opposite sign since the arbs were
                # switched
                sign = -sign1
            else:
                # Since the Arb objects have the same sign, either can be used
                sign = sign1
            digits, dp = Arb.__truesub__(digits1, dp1, digits2, dp2)
        else:
            # Since when the signs are the opposite the behavior of subtraction
            # becomes the same as that of addition, we can use addition and set
            # the sign to be that of the first Arb object
            sign = sign1
            digits, dp = Arb.__trueadd__(digits1, dp1, digits2, dp2)

        return Arb.new(digits, dp, sign)

    def __mul__(arb1, arb2):

        if not isinstance(arb2, Arb):
            raise Exception("Cannot perform subtraction on non Arb type")

        # Gets the arbitrary precision for the Arb objects
        digits1, dp1 = arb1.__round__(Arb.PRECISION)
        digits2, dp2 = arb2.__round__(Arb.PRECISION)

        return Arb.new(*Arb.__truemul__(digits1, dp1, digits2, dp2))


if __name__ == "__main__":

    Arb.PRECISION = 20

    def gen_num():
        num = ""
        length = random.randint(1, 40)
        dp = random.randint(0, length)
        for i in range(length):
            num += str(random.randint(0, 9))
        num = num[:dp] + "." + num[dp:]
        return num

    import random
    while True:

        arb1 = Arb(gen_num())
        arb2 = Arb(gen_num())
        if random.randint(0, 1):
            ans = arb1 * arb2
            actualans = Arb(float(arb1) * float(arb2))
            print(f"{arb1} * {arb2} = {ans}")
        else:
            ans = arb1 * arb2
            actualans = Arb(float(arb1) * float(arb2))
            print(f"{arb1} * {arb2} = {ans}")
        print("Actual answer is", actualans)
        if ans != actualans:
            print("  !! NOT EQUAL ------------------------")
        input()
