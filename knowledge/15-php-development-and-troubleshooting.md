# PHP — Complete Practical Foundation

- **Document ID:** KB-PHP-15
- **Status:** general technical guidance
- **Applies to:** PHP CLI, local web development, Apache/Nginx, databases and Windows
- **Keywords:** PHP, Composer, PHP-FPM, Apache, Nginx, PDO, Laravel, syntax error, fatal error, undefined variable, PHP ei toimi, palvelinpuolen ohjelmointi

## 1. What PHP does

PHP is a server-side scripting language commonly used to generate web pages and build APIs. The server executes PHP; the browser normally receives HTML, CSS and JavaScript rather than the PHP source.

A request typically flows: browser → web server → PHP runtime/application → database or other services → HTTP response.

## 2. Install and verify

Use an official PHP distribution or a maintained development environment suitable for the operating system. On Windows, ensure the PHP executable directory is on PATH if using the CLI.

```powershell
php -v
php --ini
php -m
php -l .\index.php
```

- `php -v`: version.
- `php --ini`: active configuration file.
- `php -m`: loaded extensions.
- `php -l`: syntax check without executing the file.

For web hosting, PHP must be connected to a supported web server setup. Installing the CLI alone does not make a website available.

## 3. First PHP program

```php
<?php
declare(strict_types=1);

$name = "Ada";
echo "Hello, " . htmlspecialchars($name, ENT_QUOTES, 'UTF-8');
```

PHP variables begin with `$`. Statements commonly end with semicolons. Use `<?php` for PHP code. Escape untrusted text before inserting it into HTML.

## 4. Core language concepts

- Variables: `$count = 3;`
- Types: int, float, string, bool, array, object, null.
- Conditions: `if`, `elseif`, `else`, `match`.
- Loops: `foreach`, `for`, `while`.
- Functions: named functions, parameters, return types.
- Arrays: indexed and associative.
- Classes: properties, methods, constructors, visibility and inheritance.
- Exceptions: `try`, `catch`, `finally`.
- Namespaces and autoloading organize larger applications.

Prefer strict comparisons (`===`) where appropriate. Validate external input; never assume a browser form is trustworthy.

## 5. Forms and HTTP

A form may submit using GET or POST. Read request data from the appropriate superglobal, validate it, and return a suitable response. Do not echo raw user input into HTML.

```php
<?php
$name = trim($_POST['name'] ?? '');
if ($name === '' || mb_strlen($name) > 80) {
    http_response_code(400);
    exit('Invalid name');
}
echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8');
```

Use CSRF protection for state-changing browser forms, authentication and authorization checks for protected actions, and secure session-cookie settings.

## 6. Database access with PDO

Use prepared statements. Never build SQL by concatenating untrusted input.

```php
$stmt = $pdo->prepare('SELECT id, display_name FROM users WHERE id = :id');
$stmt->execute(['id' => $userId]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
```

Use least-privilege database accounts, keep credentials outside source control, handle exceptions safely and avoid exposing SQL details to end users.

## 7. Composer

Composer manages PHP dependencies and autoloading.

```powershell
composer --version
composer init
composer require vendor/package
composer install
composer validate
```

Commit `composer.json` and `composer.lock` for applications. `composer install` installs locked versions; `composer update` intentionally recalculates dependency versions and should be reviewed.

## 8. Common errors

- **Parse error:** unmatched braces, quotes, parentheses or missing syntax. Use `php -l`.
- **Undefined variable / array key:** initialize values and validate request data.
- **Call to undefined function:** required extension not enabled, wrong PHP runtime or misspelled function.
- **Class not found:** namespace/import/autoload issue; inspect Composer configuration and run `composer dump-autoload`.
- **Database connection refused:** check service status, host, port, credentials, database and network.
- **PDO driver not found:** enable/install the correct PDO driver for the active PHP configuration.
- **HTTP 500:** inspect server-side logs; do not expose stack traces in production.
- **Permission denied:** check the web-server account's access to required files; do not grant broad write access to the whole project.
- **Works in CLI but not browser:** CLI and web server may use different PHP versions or php.ini files. Compare `php --ini` with the web runtime's configuration.

## 9. Security checklist

- Keep PHP and dependencies supported and patched.
- Escape output according to context; HTML escaping is not SQL protection.
- Use prepared SQL statements.
- Hash passwords with `password_hash()` and verify with `password_verify()`.
- Use secure session handling and regenerate session IDs after login.
- Validate uploads by content, size and allowed type; store them outside executable web paths.
- Disable detailed errors for public production responses; log safely on the server.
- Never commit secrets or display them in error messages.
