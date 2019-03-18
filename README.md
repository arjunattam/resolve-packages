# resolve-packages

Script to resolve npm package versions to commits.

## Usage

Setup dependencies (requires pipenv):

```
pipenv
```

To run on a specific package version (for `request@2.88.0`):

```
pipenv run python resolve_npm.py request 2.88.0
```

To download [most depended upon packages](https://www.npmjs.com/browse/depended) and run all:

```
pipenv run python resolve_npm.py
```

To run with GitHub PAT, set a environment variable `GITHUB_TOKEN` with the PAT, and then run the same script.

## Output

Example output on most depended upon packages (32/36 resolved):

```
lodash: 4.17.11 resolved to 0843bd46ef805dd03c0c8d804630804f3ba0ca3c
request: 2.88.0 resolved to 642024036379239a7fa29c27ef7bb4dd3fa3b3a4
chalk: 2.4.2 resolved to 9776a2ae5b5b1712ccf16416b55f47e575a81fb9
react: 16.8.4 resolved to d8a73b5eb6c7217850103193635ff1b556925ed5
express: 4.16.4 resolved to dc538f6e810bd462c98ee7e6aae24c64d4b1da93
commander: 2.19.0 resolved to 78b7dbd18aabc23ccc9d151db411913237a3c483
moment: 2.24.0 resolved to 96d0d6791ab495859d09a868803d31a55c917de1
async: 2.6.2 resolved to eaf32be0e94f62fddc83d8550814e30a4be66a3c
debug: 4.1.1 resolved to 68b4dc8d8549d3924673c38fccc5d594f0a38da1
bluebird: 3.5.3 resolved to 50bc72e561f55c4e4118988186516ee19d18cf28
prop-types: 15.7.2 resolved to 953ed9beb0f15498cd7e6e25c90f7cadd5f2149a
react-dom: 16.8.4 resolved to d8a73b5eb6c7217850103193635ff1b556925ed5
fs-extra: 7.0.1 resolved to a32c85282185aa008759890cce059594e4348262
underscore: 1.9.1 resolved to ae037f7c41323807ae6f1533c45512e6d31a1574
axios: 0.18.0 resolved to d59c70fdfd35106130e9f783d0dbdcddd145b58f
tslib: 1.9.3 resolved to 9dd9aa322c893e5e0b3f1609b1126314ccf37bbb
uuid: 3.3.2 resolved to fe4ae79c55af2c7cbf2bb39d3bcb6716d5367091
mkdirp: 0.5.1 resolved to d4eff0f06093aed4f387e88e9fc301cb76beedc7
classnames: found repo, cannot resolve to commit
body-parser: 1.18.3 resolved to e6ccf98015fece0851c0c673fc2776c30ad79e5d
glob: 7.1.3 resolved to 8882c8fccabbe459465e73cc2581e121a5fdd25b
babel-runtime: found repo, cannot resolve to commit
colors: 1.3.3 resolved to b63ef88e521b42920a9e908848de340b31e68c9d
yargs: 13.2.2 resolved to e7f29379707f9e3d5eb6edc09ba278f53cc7db74
webpack: 4.29.6 resolved to 685a0626cb10664133ef2fb2e2f9f4cb3971402a
rxjs: 6.4.0 resolved to d3e7e3f299e277b077602d26c59dab40ef0e1dba
vue: 2.6.9 resolved to 43115e09e98d484a35f7c12249396b6d5d66c7ff
jquery: 3.3.1 resolved to 32b00373b3f42e5cdcb709df53f3b08b7184a944
minimist: 1.2.0 resolved to dc624482fcfec5bc669c68cdb861f00573ed4e64
inquirer: found repo, cannot resolve to commit
babel-core: found repo, cannot resolve to commit
yeoman-generator: 3.2.0 resolved to 3bbeef0f8eebd02e9459734c9a3d9c6732a47d14
through2: 3.0.1 resolved to d0696e4be57337c5742ac6fe9d20892a2ab78b2e
aws-sdk: 2.423.0 resolved to aca7cf991add5fb7fcb98aebaf08edf421094a47
redux: 4.0.1 resolved to c5d87d95f3b9b0ebdb57791f69b53d8507cebbed
babel-loader: 8.0.5 resolved to 20c9e0eef9e62e7041a42c71509486cc44bbcb5a
```
