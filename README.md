# apply2jobs

Automate your job applications! Simply configure your job searches and personal information! Provide your resume, and let [Mistral AI](https://mistral.ai/) generate your cover letters!

## Synopsis

### Usage

```sh
src/main.py [-h] [--config CONFIG]
            [--storage-backend {filesystem,mongodb,postgresql}] [--storage-uri STORAGE_URI]
            [--resume-pdf RESUME_PDF] [--cover-letter-dir COVER_LETTER_DIR]
```

### Options

| Option                    | Arguments                         | Description                     | Default |
| ------------------------- | --------------------------------- | ------------------------------- | ------- |
| `-h`, `--help`            |                                   | Show this help message and exit |                                 |
| `-c`, `--config`          | `CONFIG`                          | Config file                     | `config.yaml`                   |
| `-s`, `--storage-backend` | `{filesystem,mongodb,postgresql}` | Storage backend                 | `filesystem`                    |
| `-l`, `--storage-uri`     | `STORAGE_URI`                     | Storage connection URI          | `file://${PWD}/apply2jobs.data` |
| `--resume-pdf`            | `RESUME_PDF`                      | Resume PDF                      | `resume.pdf`                    |
| `--cover-letter-dir`      | `COVER_LETTER_DIR`                | Coverletter directory           | `coverletters/`                 |

## Configuration

For an example configuration file, see [`etc/config.example.yaml`](./etc/config.example.yaml).

### Environment Variables

| Variable                       | Description             | Example                         |
| ------------------------------ | ----------------------- | ------------------------------- |
| `APPLY2JOBS_CONFIG`            |  Config file            | `etc/config.yaml`               |
| `APPLY2JOBS_STORAGE_BACKEND`   |  Storage backend        | `filesystem`                    |
| `APPLY2JOBS_STORAGE_URI`       |  Storage connection URI | `file:///data/apply2jobs`       |
| `APPLY2JOBS_RESUME_PDF`        |  Resume PDF             | `path/to/resume.pdf`            |
| `APPLY2JOBS_COVER_LETTERS_DIR` |  Coverletter directory  | `path/to/cover-letters/`        |
| `MISTRAL_API_KEY`              | Mistral.ai API Key      | `XXXX.YYYY.ZZZZ`                |

## Authors

- Patrick DeYoreo <<pdeyoreo@gmail.com>>
