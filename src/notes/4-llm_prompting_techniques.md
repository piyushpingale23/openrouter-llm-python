# Prompting Techniques in LLM (Large Language Models)

## Introduction

Prompting techniques are structured ways of providing instructions to an LLM so that it produces better, more accurate, and more useful responses.

Think of prompting as giving instructions to a smart assistant:

**Better Prompt → Better Output**

A good prompt should be:

- Clear
- Specific
- Context-rich
- Goal-oriented
- Format-defined, when required

---

## 1. Zero-Shot Prompting

### Definition

You ask the model to perform a task without providing any examples.

### Example

Translate this sentence into French: "I love programming."

### Use Case

Best for simple, common, and straightforward tasks.

---

## 2. One-Shot Prompting

### Definition

You provide one example before asking the model to perform the actual task.

### Example

Input: Cat  
Output: Animal

Input: Car  
Output:

### Use Case

Helps the model understand the expected pattern from a single example.

---

## 3. Few-Shot Prompting

### Definition

You provide multiple examples to help the model understand the expected pattern or task.

### Example

Input: Apple → Fruit  
Input: Dog → Animal  
Input: Rose → Flower  
Input: BMW →

### Use Case

Useful for classification, consistent response patterns, and tasks where examples help clarify the expected output.

---

## 4. Chain-of-Thought (CoT) Prompting

### Definition

You ask the model to solve step by step.

### Example

A train travels at a constant speed of 60 km per hour. How far will it travel in 5 hours? Explain the calculation.

### Use Case

Can help with multistep mathematical, logical, and reasoning tasks. However, asking for step-by-step reasoning does not guarantee a correct answer.

---

## 5. Role-Based Prompting

### Definition

You assign a specific role to the model.

### Example

Act as a senior Java developer and explain HashMap with a practical example.

---

## 6. Instruction-Based Prompting

### Definition

You provide direct instructions and clear constraints for the task.

### Example

Explain binary search in simple words using fewer than 100 words.

### Use Case

Useful when you need a specific scope, level of detail, tone, or set of constraints.

---

## 7. Contextual Prompting

### Definition

You provide relevant background information before asking the model to perform a task.

### Example

I am preparing for Java interviews and have 4 years of Java development experience. Explain important multithreading interview questions with practical examples.

### Use Case

Improves the relevance of responses by giving the model information about your background, requirements, and goals.

---

## 8. Output Format Prompting

### Definition

You specify the exact format of the response.

### Example

Explain the differences between ArrayList and LinkedList in a table.

Or:

Return valid JSON containing the fields "name", "age", and "city". Return JSON only.

### Use Case

Useful for structured responses, coding tasks, API integrations, reports, and data extraction.

---

## 9. Self-Consistency Prompting

### Definition

Ask the model to solve using multiple approaches and choose the best answer.

### Example

Solve this mathematical problem using multiple independent approaches, then compare the results to identify the most consistent answer.

### Use Case

Can improve accuracy on some reasoning tasks, particularly when multiple independent solutions can be compared. It requires additional computation and does not guarantee correctness.

---

## 10. Iterative Refinement Prompting

### Definition

You ask the model to revise and improve an initial response through one or more rounds of feedback.

### Example

Write an explanation of Java Streams. Then revise it to improve technical accuracy, clarity, and readability, while keeping it beginner-friendly.

### Use Case

Useful for improving documentation, emails, code explanations, reports, and other generated content.

---

## Real-World Example

### Bad Prompt

Explain Java.

### Good Prompt

Act as a Java trainer.

Explain the Java Collections Framework for interview preparation. Include:

- Simple explanations
- Practical Java examples
- Differences between commonly used collections
- Common interview questions

Keep the explanation beginner-friendly and technically accurate.

### Result

The improved prompt provides clearer expectations about the role, topic, audience, content, and format. This helps guide the model toward a more useful response.

---

## Key Takeaways

- **Zero-shot:** No examples.
- **One-shot:** One example.
- **Few-shot:** Multiple examples.
- **Chain-of-Thought:** Encourages intermediate reasoning.
- **Role-based:** Defines a role or perspective.
- **Instruction-based:** Defines clear instructions and constraints.
- **Contextual:** Supplies relevant background.
- **Output format:** Specifies the response structure.
- **Self-consistency:** Compares multiple candidate reasoning paths or answers.
- **Iterative refinement:** Improves a response through revision.

**Important:** These techniques can be combined in a single prompt. For example, you can define a role, provide context, include examples, specify constraints, and request a JSON response together.
