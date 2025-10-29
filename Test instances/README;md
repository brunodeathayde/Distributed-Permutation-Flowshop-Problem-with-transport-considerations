"""
Test Instance Description

This dataset comprises two categories of test instances designed for evaluating scheduling algorithms:
1. Small-sized instances
2. Large-sized instances (Extended Taillard Testbed)

Each category varies in scale, structure, and parameter combinations.
"""

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SmallSizedInstances:
    """
    🔹 Small-Sized Instances

    Compact instances designed for preliminary testing or algorithm tuning.
    """
    job_counts: List[int] = (4, 6, 8, 10, 12, 14, 16)
    machine_counts: List[int] = (2, 3, 4, 5)
    family_counts: List[int] = (2, 3, 4)
    instances_per_configuration: int = 5
    total_instances: int = 420
    processing_time_distribution: str = "Uniform[1, 100]"
    release_date_distribution: str = "Uniform[0, 5n]"
    due_date_formula: str = (
        "d_j = max(r_j) + sum(p_ij) * (1 + rand * (1/n_f) * 0.5), where rand ∈ Uniform(0, 1)"
    )

@dataclass
class LargeSizedInstances:
    """
    🔸 Large-Sized Instances (Extended Taillard Testbed)

    Adapted from the well-known Taillard benchmark and scaled for more intensive testing.
    """
    job_machine_configurations: List[Tuple[int, int]] = (
        (20, 5), (20, 10), (20, 20),
        (50, 5), (50, 10), (50, 20),
        (100, 5), (100, 10), (100, 20),
        (200, 10), (200, 20),
        (500, 20)
    )
    instances_per_configuration: int = 10
    family_counts: List[int] = (2, 3, 4, 5, 6, 7)
    total_instances: int = 720
    attributes_note: str = (
        "Based on Taillard’s structure with extended parameters for family-based scheduling. "
        "Processing times, release dates, and due dates follow the same logic as the small-sized set."
    )

@dataclass
class TestInstanceDescription:
    """
    📦 Combined Test Instance Description
    """
    small: SmallSizedInstances = SmallSizedInstances()
    large: LargeSizedInstances = LargeSizedInstances()

    def display(self):
        print("🧪 Test Instance Description\n")

        print("🔹 Small-Sized Instances")
        print(f"  • Job counts (n): {self.small.job_counts}")
        print(f"  • Machine counts (m): {self.small.machine_counts}")
        print(f"  • Family counts (nf): {self.small.family_counts}")
        print(f"  • Instances per configuration: {self.small.instances_per_configuration}")
        print(f"  • Total instances: {self.small.total_instances}")
        print("  Attributes:")
        print(f"    • Processing times (pᵢⱼ): {self.small.processing_time_distribution}")
        print(f"    • Release dates (rⱼ): {self.small.release_date_distribution}")
        print(f"    • Due dates (dⱼ): {self.small.due_date_formula}\n")

        print("🔸 Large-Sized Instances (Extended Taillard Testbed)")
        print(f"  • (Jobs × Machines) configurations: {self.large.job_machine_configurations}")
        print(f"  • Instances per configuration: {self.large.instances_per_configuration}")
        print(f"  • Family counts (nf): {self.large.family_counts}")
        print(f"  • Total instances: {self.large.total_instances}")
        print("  Attributes:")
        print(f"    • {self.large.attributes_note}")

if __name__ == "__main__":
    description = TestInstanceDescription()
    description.display()
