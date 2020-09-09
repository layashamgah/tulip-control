# Solving the memory error problem
The ``bdd.py`` script uses cache for the ``self._ite`` recursive function. 
Since there is no limit on how much memory can be used for caching, this cache grows unboundedly. As a result, we can see the memory error problem. 

## Solution Strategy 
One way to solve this problem by limiting the cache size. We can define the maximum size of the cache, and if the cache exceeds the maximum size, we can simply discard the first element of the cache. This way, we can only keep the latest cache in memory.

## How to modify cache by yourself?
Although the solution stategy looks very simple, finding the ``bdd.py`` file is cumbersome since it is not located under ``tulip-control`` directory. If you use a virtual environment for your project, first try to locate the ``dd-0.5.5-py3.6.egg`` under your ``venv`` folder. After __unziping__ this file, navigate to ``dd`` folder. You can now locate the ``bdd.py`` file and go to line number ``733`` for the ``self._ite`` recursive function.

## How to utilize  my modification?
I have created two version for solving the cache problem
* ```version_ite```: only limits the cache variable for  the ``self._ite`` recursive function. 
* ```version_bdd```: limits all cache variables in ``bdd.py`` scripts. 
  
Simply replace your ``dd-0.5.5-py3.6.egg`` with mine one. In my case, ``dd-0.5.5-py3.6.egg`` is located under ``~/anaconda3/envs/tuilp/lib/python3.6/site-packages/`` where 
* ``tuilp`` is my conda virtual environment
* I have used the following command to repalce this file
  * ``` cp  version_ite/dd-0.5.5-py3.6.egg ~/anaconda3/envs/tuilp/lib/python3.6/site-packages/ ```


That's it! You are now ready to synthesize your strategy. 
Hope this helps!

## Update
This fix makes the code run for two days and plus 
and it was killed because of the memory problem again. 
We can try ```version_bdd``` but is it worthy?
Here is the log of the execution on the server:
```
`polytope` failed to import `cvxopt.glpk`.
will use `scipy.optimize.linprog`
`omega.symbolic.symbolic` failed to import `dd.cudd`.
Will use `dd.autoref`.
Killed

real    3027m44.795s
user    2722m39.085s
sys     2m6.688s
```
