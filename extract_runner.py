from time import sleep
from raven import Client

from storage.secrets import sentry_dsn
from storage.models import Database, NoRecordsToProcessError
from utils.exceptions import TemporaryChillError
from extract.extract_location_and_date import Extractor


class ExtractRunner(object):

    def __init__(self):
        self.azureTable = Database()

    def call(self):
        transcript, partition_key = self.azureTable.retrieve_next_record_for_extraction()
        extractor = Extractor(transcript)
        location = extractor.get_location()
        date = extractor.get_date()
        print("Location: " + location)
        print("Date: " + date)
        self.azureTable.update_location_date(partition_key, location, date)


if __name__ == "__main__":
    client = Client(sentry_dsn)
    runner = ExtractRunner()

    while 1:
        try:
            runner.call()
            print("Sleeping after success")
            sleep(5)  # 5 seconds
        except NoRecordsToProcessError:
            print("Nothing to do: sleeping for five minutes")
            sleep(60 * 5)
        except TemporaryChillError as e:
            print("Temporary chill for {0} seconds".format(e.pause_time))
            client.captureException()
            sleep(e.pause_time)
        except KeyboardInterrupt as e:
            print("Interrupted by user.")
            break
        # except Exception as e:
        #     print("Error!: {0}".format(e))
        #     client.captureException()
        #     sleep(60)

