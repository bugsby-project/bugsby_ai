import os.path
import re
import tempfile

from artificial_intelligence.ai_models.severity_classifier import SeverityClassifier
from artificial_intelligence.log_parser.drain import LogParser
from artificial_intelligence.model.issue_type import IssueType
from artificial_intelligence.model.prefilled_issue import PrefilledIssue
from artificial_intelligence.model.severity import Severity
from artificial_intelligence.model.severity_level import SeverityLevel


class GradleLogParser:
    def __init__(self, severity_classifier: SeverityClassifier):
        self._severity_classifier = severity_classifier

    def analyse_log(self, title: str, received_file) -> PrefilledIssue:
        with tempfile.NamedTemporaryFile() as log_file, \
                tempfile.TemporaryDirectory() as output_dir:
            received_file.save(log_file.name)
            log_file_name = os.path.basename(log_file.name)
            input_dir = os.path.dirname(log_file.name)
            log_format = '<Date> <Content>'
            regex = []
            st = 0.5
            depth = 4

            parser = LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
            parser.parse(log_file_name)

            actual_behaviour, stack_trace = self._extract_actual_behaviour_and_stack_trace(output_dir, log_file.name)
            description = self._extract_description(actual_behaviour)
            expected_behaviour = self._extract_expected_behaviour(description)
            title_formatted = self._format_title(title)
            severity_level = self._severity_classifier.predict(title_formatted)
            severity = Severity.MAJOR if severity_level == SeverityLevel.severe else Severity.MINOR

            return PrefilledIssue(title=title_formatted,
                                  description=description,
                                  expected_behaviour=expected_behaviour,
                                  actual_behaviour=actual_behaviour,
                                  stack_trace=stack_trace,
                                  severity=severity,
                                  issue_type=IssueType.BUG)

    def _extract_actual_behaviour_and_stack_trace(self, output_dir: str, log_file_name: str) -> tuple:
        structured_file_name = os.path.join(output_dir,
                                            [f for f in os.listdir(output_dir) if re.match(r'.*_structured\.csv', f)][
                                                0])

        # extract the first 2 fail reasons
        failure_regex = re.compile('.*fail.*', re.IGNORECASE)
        failure_1, failure_2 = None, None
        with open(structured_file_name, 'r') as structured_file:
            for line in structured_file.readlines():
                if failure_regex.match(line):
                    if failure_1 is None:
                        failure_1 = line
                    elif failure_2 is None:
                        failure_2 = line
                    else:
                        break

        time_stamp_failure_1 = failure_1.split(',')[1]
        time_stamp_failure_2 = failure_2.split(',')[1]

        stack_trace_regex = re.compile(r'(?m)^.*?Exception.*(?:\n+^.*at .*)+')

        # extract the fail reason based on the unique timestamp
        actual_behaviour, stack_trace, to_append = '', '', False

        with open(log_file_name, 'r') as log_file:
            content = log_file.read()

            for line in content.split('\n'):
                if line.startswith(time_stamp_failure_1):
                    actual_behaviour = line
                    to_append = True
                elif line.startswith(time_stamp_failure_2):
                    actual_behaviour += '\n' + line
                    break
                elif to_append:
                    actual_behaviour += '\n' + line

            match = stack_trace_regex.search(content)
            if match:
                stack_trace = match.group()

        return actual_behaviour, stack_trace

    def _extract_description(self, task_failed_description: str) -> str:
        lines = task_failed_description.split('\n')
        # extract the failed Gradle task
        task_regex = re.compile('.*Task.*', re.IGNORECASE)

        task_failed_lines = list(filter(lambda x: task_regex.match(x), lines))
        task_failed_line = task_failed_lines[0] if task_failed_lines else ''
        return ' '.join(task_failed_line.split(' ')[1:])

    def _extract_expected_behaviour(self, description: str) -> str:
        if description == '':
            # default expected behaviour
            return 'Pipeline run should have been SUCCESSFUL'

        return ' '.join(description.split(' ')[0:-1]) + ' should have been SUCCESSFUL'

    def _format_title(self, title: str) -> str:
        return title + ' has failed'
