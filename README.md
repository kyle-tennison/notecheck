# notecheck

A utility for identifying grammatical and conceptual errors in Markdown notes using OpenAI's language models.

## Installation

Clone the repository and install the package:

```bash
pip install .
```

Then, create a `.env` file containing your OpenAI API key:

```
OPENAI_API_KEY=your-key-here
```

## Usage

To run the checker:

```bash
notecheck path/to/notes/root
```

By default, the path is set to `~/obsidian/notes`, but this may vary depending on your system.

The tool will:
- Automatically correct basic grammatical and spelling issues.
- Annotate more complex or conceptual issues with comments for review.

## Example

Below is a sample input containing a conceptual error:

---

You can represent the internal energy and enthalpy of a gas from its constituent gases using the mole fractions:

$$\bar u = \sum_i y_i\bar u_i \quad \text{and} \quad \bar h = \sum_i y_i \bar h_i$$

This also carries over to specific heats:

$$\bar c_v = \sum_i y_i \bar c_{v,i} \quad \text{and} \quad \bar c_p = \sum_i y_i \bar c_{p,i}$$

Remember that:

$$\bar c_v = \bar c_p + \bar R \tag{ideal gas}$$

> 🤖 (notecheck comment) — For an ideal gas, the correct relationship is $c_p = c_v + R$, not $c_v = c_p + R$.

---

The comment highlights the error, allowing you to review and correct the note accordingly.