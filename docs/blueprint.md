# **App Name**: MutationWatch

## Core Features:

- Git URL Intake: Accept a Git URL from the frontend.
- Repository Cloning & WebSocket Setup: Clone the repository from the provided Git URL and establish a WebSocket connection to the frontend to provide status updates.
- Language Detection: Analyze the repository to identify the programming language. Only proceed if the language is PHP.
- Mutation Testing Execution: Execute `vendor/bin/infection` and `vendor/bin/phpunit` commands to perform mutation testing using the Infection library and PHPUnit.
- Test Case Suggestion (AI-Powered): Analyze surviving mutants to identify weak spots in the test suite. Use an AI tool to generate basic test case stubs based on the uncovered mutants, to provide a basis for developer improvement.

## Style Guidelines:

- Primary color: Deep blue (#1A237E) for a professional look.
- Secondary color: Light gray (#ECEFF1) for backgrounds and content separation.
- Accent: Teal (#26A69A) for highlighting key information and interactive elements.
- Clean and readable sans-serif font for code snippets and results.
- Simple, clear icons to represent status updates and actions.
- Well-structured layout with clear sections for input, processing, and results.

## Original User Request:
saya ingin membuat server backend berbasis mutation testing dengan fitur berikut
1. frontend kirim git url
2. backend akan memproses url dan clone repository tersebut, dan mengirimkan link websocket connection
3. backend akan memproses repository dan mengenali bahasa pemrograman, jika selain php maka tertolak, jika php maka akan menuju proses selanjutnya
4. backend akan melakukan command berikut dengan library infection dan phpunit dari php
vendor/bin/infection
vendor/bin/phpunit
5. backend akan mengenali mutant mana yang belum ter-kill dan membuat test case berdasarkan itu (buat method/function abstraksinya saja jika fitur ini terlalu rumit)
6. setelah selesai kirimkan notifikasi melalui websocket yang sudah terjadi pada proses 2

Buat dalam bahasa pemrograman apapun, menurut saya akan lebih mudah dengan python flask karena tahap 5 memerlukan algortma genetika dan python sangat mendukung untuk itu
  