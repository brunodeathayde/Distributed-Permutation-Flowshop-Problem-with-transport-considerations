# 🧪 Test Instance Description

This dataset comprises two categories of test instances designed for evaluating scheduling algorithms:

1. **Small-sized instances**
2. **Large-sized instances** (Extended Taillard Testbed)

Each category varies in scale, structure, and parameter combinations.

---

## 🔹 Small-Sized Instances

Compact instances designed for preliminary testing or algorithm tuning.

### Configuration
- **Job counts (n):** 4, 6, 8, 10, 12, 14, 16  
- **Machine counts (m):** 2, 3, 4, 5  
- **Family counts (nf):** 2, 3, 4  
- **Instances per configuration:** 5  
- **Total instances:** 420  

### Attributes
- **Processing times (pᵢⱼ):** Uniform distribution in [1, 100]  
- **Release dates (rⱼ):** Uniform distribution in [0, 5n]  
- **Due dates (dⱼ):**  
  \[
  d_j = \max(r_j) + \sum p_{ij} \cdot \left(1 + \text{rand} \cdot \left(\frac{1}{n_f}\right) \cdot 0.5\right)
  \]  
  where rand ∈ Uniform(0, 1)

---

## 🔸 Large-Sized Instances (Extended Taillard Testbed)

Adapted from the well-known Taillard benchmark and scaled for more intensive testing.

### Configuration
- **(Jobs × Machines):**  
  (20×5), (20×10), (20×20)  
  (50×5), (50×10), (50×20)  
  (100×5), (100×10), (100×20)  
  (200×10), (200×20)  
  (500×20)  
- **Instances per configuration:** 10  
- **Family counts (nf):** 2, 3, 4, 5, 6, 7  
- **Total instances:** 720  

### Attributes
- Based on Taillard’s structure with extended parameters for family-based scheduling  
- Processing times, release dates, and due dates follow the same logic as the small-sized set

---

## 📁 Repository Structure

| File | Description |
|------|-------------|
| `README.md` | Dataset overview and configuration details |
| `data/` | Folder containing instance files (if applicable) |
| `scripts/` | Optional scripts for loading or analyzing instances |

---

## 📬 Contact

For questions or collaboration, feel free to reach out to:  
**BRUNO** – baprata@ufc.br
