title: 자주쓰는 git 명령 정리
date: 2018-03-09
category: tool
tags: git
slug: gitcmd

git을 안쓰는 개발자가 거의 없을 정도로 git은 버전 컨트롤 시스템 (Version Control System)을 대표하게 되었습니다. 예전에는 ftp, svn을 많이 사용했었던 기억이 납니다.

이 포스트에서는 자주 사용하는 git 명령들을 정리해 보았습니다.

## remote
- add remote
`git remote add origin <url>`

- change remote
`git remote set-url origin <url>`

- remove remote
`git remote -v`
`git remote rm <destination>`

## commit, push, fetch, pull
- push forcely
`git push origin master --force`
`git push origin master -f`
 
- pull forcely
`git fetch --all`
`git reset --hard origin/master`

​- fetch file forcely
`git fetch`
`git checkout origin/master <filepath>`
​
- cancel commit
`git reset HEAD~`

## config
- cache
`git config --global credential.helper "cache --timeout=86400"`

- logout
`echo -e "host=github.com\nprotocol=https\n" | git credential-osxkeychain erase`
`git config --global --unset user.name`
`git config --global --unset user.email`

## add only py
`git add ./\*.py`
 
## create branch
`git checkout -b [name_of_your_new_branch]`
​
## rename branch
`git push <REMOTENAME> <LOCALBRANCHNAME>:<REMOTEBRANCHNAME>`
​
## remove local branch
`git branch -d the_local_branch`
​
## remove remote branch
`git push origin :the_remote_branch`

## sparse
`git init`
`git remote add -f origin <url>`
`git config core.sparseCheckout true`

`echo "some/dir/" >> .git/info/sparse-checkout`

## checkout
`git checkout <branch>`
`git pull`

## push branch
`git push origin <branch_from>:<branch_to>`
