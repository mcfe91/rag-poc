import random

from loguru import logger
from pydantic import BaseModel

class InstructDatasetSample(BaseModel):
    instruction: str
    answer: str

class InstructDataset(BaseModel):
    train: list[InstructDatasetSample]
    validation: list[InstructDatasetSample]
    test: list[InstructDatasetSample]
    val_split_ratio: float
    test_split_ratio: float
    seed: int | None = None

    @classmethod
    def from_samples(
        cls,
        samples: list[InstructDatasetSample],
        val_split_ratio: float,
        test_split_ratio: float,
        seed: int | None = None,
    ) -> "InstructDataset":
        """Creates an InstructDataset by splitting samples into train/val/test sets.

        Args:
            samples: List of samples to split
            val_split_ratio: Ratio of samples to use for validation (between 0 and 1)
            test_split_ratio: Ratio of samples to use for testing (between 0 and 1)
            seed: Random seed for shuffling. If None, no fixed seed is used.

        Returns:
            InstructDataset with shuffled and split samples
        """

        shuffled_samples = samples.copy()

        if seed is not None:
            random.seed(seed)
        random.shuffle(shuffled_samples)

        train_samples = shuffled_samples[
            : int(len(shuffled_samples) * (1 - val_split_ratio - test_split_ratio))
        ]
        val_samples = shuffled_samples[
            int(len(shuffled_samples) * (1 - val_split_ratio - test_split_ratio)) : int(
                len(shuffled_samples) * (1 - test_split_ratio)
            )
        ]
        test_samples = shuffled_samples[
            int(len(shuffled_samples) * (1 - test_split_ratio)) :
        ]

        logger.info(
            "Created dataset with the following splits: "
            f"- Train samples: {len(train_samples)}, "
            f"- Validation samples: {len(val_samples)}, "
            f"Test samples: {len(test_samples)}"
        )

        assert len(train_samples) > 0, "Train split must have at least one sample"
        assert len(val_samples) > 0, "Validation split must have at least one sample"
        assert len(test_samples) > 0, "Test split must have at least one sample"

        return InstructDataset(
            train=train_samples,
            validation=val_samples,
            test=test_samples,
            val_split_ratio=val_split_ratio,
            test_split_ratio=test_split_ratio,
            seed=seed,
        )