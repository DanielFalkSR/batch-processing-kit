# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import List

from batch_client.batch_request import BatchRequest
from batch_client.speech_sdk.work_item import SpeechSDKWorkItemRequest
from batch_client.utils import BadRequestError
from batch_client.work_item import WorkItemRequest


class SpeechSDKBatchRequest(BatchRequest):
    def __init__(self, files: List[str],
                 language: str, diarization: str, nbest: int, profanity: str,
                 allow_resume: bool, enable_sentiment: bool, combine_results: bool = False):
        super().__init__(files, combine_results)
        # TODO: We need to support all the options available on the
        #       Azure Cognitive Services on-cloud batch service.
        self.language = language
        self.diarization = diarization
        self.nbest = nbest
        self.profanity = profanity
        self.allow_resume = allow_resume
        self.enable_sentiment = enable_sentiment

    def make_work_items(self, output_dir: str,
                        cache_search_dirs: List[str],
                        log_dir: str) -> List[WorkItemRequest]:
        return [
            SpeechSDKWorkItemRequest(
                f,
                self.language,
                self.nbest,
                self.diarization,
                self.profanity,
                cache_search_dirs,
                output_dir,
                log_dir,
                self.allow_resume,
                self.enable_sentiment,
            )
            for f in self.files
        ]

    @staticmethod
    def from_json(json: dict):
        for arg in ['files', 'language', 'diarization', 'nbest', 'profanity', 'combine_results']:
            if arg not in json:
                raise BadRequestError("Missing '{arg}' argument in request body".format(arg=arg))
        if not isinstance(json['files'], list) or \
                not all([isinstance(x, str) for x in json['files']]):
            raise BadRequestError("Request body argument 'files' was not List[str]")
        return SpeechSDKBatchRequest(json['files'], json['language'], json['diarization'],
                                     json['nbest'], json['profanity'], bool(json['combine_results']))