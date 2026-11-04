# C# and .NET — Complete Practical Foundation

- **Document ID:** KB-CSHARP-17
- **Status:** general technical guidance
- **Applies to:** C#, .NET SDK, console apps, desktop apps, web APIs and Visual Studio
- **Keywords:** C#, C Sharp, .NET, dotnet CLI, SDK, runtime, NuGet, class, async await, exception, nullable, build error, C# ohjelmointi

## 1. C# and .NET

C# is a strongly typed, object-oriented language. .NET provides the runtime, base libraries, SDK, build tools and application frameworks. The SDK is used to create, build, test and publish projects; the runtime runs applications.

Check installed versions:

```powershell
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
```

Use a supported .NET release and match the target framework required by the project.

## 2. Create and run a console app

```powershell
dotnet new console -n HelloApp
cd HelloApp
dotnet run
dotnet build
dotnet test
```

A basic program:

```csharp
Console.WriteLine("Hello, world!");
```

Modern .NET supports top-level statements. Older templates may show an explicit `Program` class and `Main` method.

## 3. Language fundamentals

- Variables and types: `int`, `double`, `decimal`, `bool`, `char`, `string`.
- Type inference: `var` infers a compile-time type; it does not make the variable dynamically typed.
- Control flow: `if`, `switch`, `for`, `foreach`, `while`.
- Methods: parameters, return values, overloads and optional parameters.
- Collections: arrays, `List<T>`, `Dictionary<TKey,TValue>`, interfaces such as `IEnumerable<T>`.
- OOP: classes, objects, encapsulation, inheritance, interfaces and composition.
- Value/reference types, records, structs and enums.
- Generics and LINQ.
- Exceptions and resource cleanup with `using`.

## 4. Nullability and safe code

Enable nullable reference types where appropriate. Treat compiler warnings seriously. Use validation at boundaries instead of assuming input is valid.

```csharp
string? nickname = null;
string displayName = nickname ?? "Guest";
```

The null-forgiving operator suppresses a warning; it does not make a null value safe.

## 5. Async and await

Use asynchronous APIs for I/O-bound work such as HTTP and database operations. Await tasks rather than blocking threads with `.Result` or `.Wait()` in ordinary application code.

```csharp
using System.Net.Http;

using var client = new HttpClient();
string body = await client.GetStringAsync("https://example.com");
Console.WriteLine(body.Length);
```

Handle cancellation and exceptions. Do not create unnecessary async wrappers around purely synchronous work.

## 6. NuGet and project files

NuGet manages .NET packages. Package references are commonly recorded in the `.csproj` file.

```powershell
dotnet add package Package.Name
dotnet restore
dotnet list package
dotnet remove package Package.Name
```

Review package compatibility, licensing, maintenance and transitive dependencies before adding libraries.

## 7. Testing and publishing

Use a test framework such as xUnit, NUnit or MSTest selected by the project. Keep unit tests deterministic and isolate external services.

```powershell
dotnet test
dotnet publish -c Release
```

Publishing output is not the same as installing the .NET runtime on every target machine; choose framework-dependent or self-contained deployment intentionally.

## 8. Common problems

- **dotnet not recognized:** install the SDK, reopen terminal and inspect PATH.
- **SDK not found / wrong target framework:** inspect `global.json`, installed SDKs and project `TargetFramework`.
- **Build fails after package update:** inspect NuGet restore output and package compatibility; revert or pin versions deliberately.
- **Namespace/type not found:** check project references, namespace, using directives and spelling.
- **NullReferenceException:** inspect the failing value and validate assumptions; do not silence nullability warnings blindly.
- **InvalidOperationException:** inspect the operation's required state and call sequence.
- **Port already in use:** identify the process using the port and configure the app's listening URL.
- **Works in IDE but not terminal:** compare selected SDK, environment variables, working directory and launch profile.
- **Async deadlock or unresponsive UI:** avoid sync-over-async and use async APIs appropriately.
- **File not found:** remember that relative paths are resolved against the process working directory, not necessarily the source file directory.

## 9. Security and maintainability

Validate external input, use parameterized database queries, protect secrets with environment-specific secret storage, keep dependencies updated, and avoid logging credentials or personal data. Prefer composition and small testable classes over unnecessary inheritance.
