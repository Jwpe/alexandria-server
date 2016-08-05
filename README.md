# alexandria-server

This repository contains the server element of the work-in-progress Alexandria documentation service.

`alexandria-server` is responsible for authentication of users with GitHub, issuing authorization tokens, and managing user, organization and project data.

The project is currently in a very early alpha stage and as such all APIs will be changing rapidly. Please do not rely on anything in this repository until the first official release.

## Local development

`alexandria-server` requires [Docker](https://docs.docker.com/engine/installation/) 1.11 and `docker-compose` version 1.5 or above to run locally.

To run the server, set up a `.env` file in the root directory of the project containing the following environment variables:

```bash
SECRET_KEY=a_super_secret_key
GITHUB_CLIENT_ID=123456789
GITHUB_CLIENT_SECRET=123456789abcde
```

`SECRET_KEY` provides Django with a secret key for hashing and other security purposes. The GitHub settings should be copied from an OAuth application which you can register on GitHub at https://github.com/settings/applications/new

You'll need to run the initial database migrations as follows:

```bash
docker-compose run server python manage.py migrate
```

The server is then run with the `docker-compose up` command.

In order to correctly recieve callbacks from the GitHub OAuth flow, you will need to expose your local port 80 to a secure online address. You can do this using the [`ngrok` service](https://ngrok.com) or any software able to set up a secure local tunnel. Don't forget to add the tunnel's URL to your OAuth application's callback URL on GitHub!

## Contributing

Contributions to `alexandria-server`s development are welcome. Please feel free to open an issue or submit a pull request: contributing guidelines will follow soon.

## License

This software is licensed under the MIT License. See [LICENSE](LICENSE).