class Solution:
    symbol_values = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }

    def romanToInt(self, s: str) -> int:
        int_val = 0
        idx = 0

        # word_total = 0
        # sub_vals = []
        # word_vals = [self.symbol_values[x] for x in s]
        # print(word_vals)
        # for idx, val in enumerate(word_vals[::-1]):
        #     # hold 1 to check for following larger values
        #     if val == 1:
        #         sub_vals.append((idx, val))
        #     # check to see if there are held values
        #     if len(sub_vals) > 0:
        #         for x in sub_vals:
        #             if x[0] == idx-1:
        #                 if x[1] < val:
        #                     word_total += val-1

            

        while idx < len(s):
            if s[idx] == "C":
                # contains C subtraction
                if (idx + 1 < len(s)) and (s[idx + 1] == "M"):
                    int_val += 900
                    idx += 2
                elif (idx + 1 < len(s)) and (s[idx + 1] == "D"):
                    int_val += 400
                    idx += 2
                # normal C
                else:
                    int_val += self.symbol_values["C"]
                    idx += 1
            elif s[idx] == "X":
                # contains X subtraction
                if (idx + 1 < len(s)) and (s[idx + 1] == "C"):
                    int_val += 90
                    idx += 2
                elif (idx + 1 < len(s)) and (s[idx + 1] == "L"):
                    int_val += 40
                    idx += 2
                # normal X
                else:
                    int_val += self.symbol_values["X"]
                    idx += 1
            elif s[idx] == "I":
                # contains I subtraction
                if (idx + 1 < len(s)) and (s[idx + 1] == "X"):
                    int_val += 9
                    idx += 2
                elif (idx + 1 < len(s)) and (s[idx + 1] == "V"):
                    int_val += 4
                    idx += 2
                # normal I
                else:
                    int_val += self.symbol_values["I"]
                    idx += 1
            # normal M,D,L,V
            else:
                int_val += self.symbol_values[s[idx]]
                idx += 1

        return int_val


if __name__ == "__main__":
    sol = Solution()
    
    # while roman_numeral_input := input("Enter Roman numeral: "):
    #     if not roman_numeral_input.isalpha() or all(i.upper() not in sol.symbol_values for i in roman_numeral_input):
    #         continue
    #     break
    # print(sol.romanToInt(roman_numeral_input.upper()))

    for roman_numeral_input in [
        "XVII",  # 17
        "XIX",  # 19 not 21
        "XCVIII",  # 98
        "CIC",  # 199 not 201
        "CMXCVIII",  # 998
        "CMIC",  # 999?
        "DID",  # 999? same as IM?
        "IM",  # 999? same as DID?
    ]:
        print(sol.romanToInt(roman_numeral_input.upper()))
