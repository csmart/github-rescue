So let me be clear here, I don't think it's a bad thing that Microsoft bought
GitHub. No one is forcing you to use their services, in fact they make it
trivial to stop using them. So what's the big deal.

I've posted about a few git mirror scripts I run at home recently: one to
[mirror gerrit
repos](http://www.madebymikal.com/how-to-maintain-a-local-mirror-of-onaps-git-repositories/);
and one to [mirror arbitrary GitHub
users](http://www.madebymikal.com/how-to-maintain-a-local-mirror-of-github-repositories/).

It was therefore trivial to whip up a slightly nicer script intended to help
you forklift your repos out of GitHub if you're truly concerned. It's posted on
GitHub now (irony intended).

Generate yourself a [GitHub
token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
and you can just do something like:

```bash
$ sudo pip install -U -r requirements.txt
$ python ./download.py --github_token=foo --username=mikalstill
```

I intend to add support for auto-creating and importing GitLab repos into the
script, but haven't gotten around to that yet. Pull requests welcome.


