from .constants import HIGH_NUM_OF_FILES_THRESHOLD, LOW_NUM_OF_FILES_THRESHOLD, COMPANY_DOMAIN, VENDOR_DOMAINS, \
    PRIORITY_PREFIX, Priority, PRIORITY_TO_SCORE, DEFAULT_PRIORITY_SCORE


class Amy:
    """
    # Task 1
    Amy prioritize the email according the following characteristics:
    1. Title contains the word "priority:<PRIORITY_LEVEL>". PRIORITY_LEVEL might be one of the following: [low | medium | high].
    if the email doesn't contain the word, it should be considered as low
    2. Number of attached files in the email - above 10 is high, between 5 and 10 is medium and below 5 is low
    3. by sender - the company's employees are more important than the company's vendor that more important from the rest.
    assuming the domain of the company is "company" and the vendor is "vendor"

    Amy uses the subject, num of attached files and the sender address of the email
    The total priority score is the weighted sum of the characteristics above:
    0.5*subject_priority_score + 0.3*sender_priority_score + 0.2*attached_files_priority_score
    """

    def calculate_priority_score(self, email_properties) -> float:
        score = 0.5 * self.calculate_subject_priority_score(email_properties['subject']) + \
                0.3 * self.calculate_sender_priority_score(email_properties['sender']) + \
                0.2 * self.calculate_attached_files_priority_score(email_properties['num_of_files'])

        return round(score, 2)

    def calculate_subject_priority_score(self, subject) -> float:
        priority_level = Priority.low

        if PRIORITY_PREFIX in subject:
            subject_priority_index = subject.index(PRIORITY_PREFIX)
            priority = subject[subject_priority_index + len(PRIORITY_PREFIX):].split(' ')[0]
            priority_level = Priority.from_str(priority)

        return PRIORITY_TO_SCORE.get(priority_level, DEFAULT_PRIORITY_SCORE)

    def calculate_attached_files_priority_score(self, num_of_files) -> float:
        priority_level = Priority.low

        if num_of_files > HIGH_NUM_OF_FILES_THRESHOLD:
            priority_level = Priority.high
        elif LOW_NUM_OF_FILES_THRESHOLD <= num_of_files <= HIGH_NUM_OF_FILES_THRESHOLD:
            priority_level = Priority.medium

        return PRIORITY_TO_SCORE.get(priority_level, DEFAULT_PRIORITY_SCORE)

    def calculate_sender_priority_score(self, sender) -> float:
        priority_level = Priority.low

        if '@' in sender:
            domain_start_index = sender.index('@')
            domain = sender[domain_start_index + 1:]

            if domain == COMPANY_DOMAIN:
                priority_level = Priority.high
            elif domain in VENDOR_DOMAINS:
                priority_level = Priority.medium

        return PRIORITY_TO_SCORE.get(priority_level, DEFAULT_PRIORITY_SCORE)
