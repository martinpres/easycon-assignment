from dataclasses import dataclass


@dataclass(frozen=True)
class RecordMetadata:
    topic: str
    mongo_id: str
    created_at: str

    @staticmethod
    def from_tuple(given):
        # given[0] is the id
        return RecordMetadata(given[1], given[2], given[3])

    def to_dict(self):
        return {
            'topic': self.topic,
            'mongo_id': self.mongo_id,
            'created_at': self.created_at,
        }
