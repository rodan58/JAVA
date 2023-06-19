import matplotlib.pyplot as plt


class Post:
    def __init__(self, file):
        self.emails = {}
        self.tot_prob = 0
        self.count_prob = 0
        self.conf = []
        for line in open(file, 'r'):
            if line.startswith("From:"):
                try:
                    self.emails[line.split()[1]] += 1
                except KeyError:
                    self.emails[line.split()[1]] = 1
            elif line.startswith("X-DSPAM-Probability:"):
                self.tot_prob += float(line.split()[1])
                self.count_prob += 1
            elif line.startswith("X-DSPAM-Confidence:"):
                self.conf.append(float(line.split()[1]))

    def check_params(self):
        print('"X-DSPAM-Probability" shows the possibility that this message is spam')
        print("--Average spam probability:", self.tot_prob / self.count_prob)
        print('"X-DSPAM-Confidence" shows our confidence that message is spam\nThe greater this parameter - the more probable that the message is spam')
        print("--Average spam confidence:", sum(self.conf) / len(self.conf))

    def calculate_spam(self):
        spamers = []
        for email, stat in zip(self.emails, self.conf):
            if stat >= 0.9:  # If confidence that this is a spam greater than 0.9 we will count it as spam
                spamers.append(email)
        print(len(set(spamers)), 'from', len(self.emails), 'are spammers:')
        for item in set(spamers):
            print(item)

    def check_users(self):
        x = []
        names = []
        for i in self.emails:
            x.append(self.emails[i])
            names.append(i)
        plt.figure(figsize=(15, 10))
        plt.barh(names, x)
        plt.show()


all_here = Post('data3.txt')
all_here.check_params()
print()
all_here.calculate_spam()
all_here.check_users()