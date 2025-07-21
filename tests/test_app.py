# File compliant with pytest
# The test methods are not dynamical, aka. their input is fixed
# This is done for convenience reasons
# And besides let me put in my catalog whatever I want and not some random stuff for once

# Due to this fixed nature, the status codes can be specified in the assertions

import pytest

# import all neccessary requirements
from tests.add_content import (
    add_movie,
    add_series,
    add_episode,
    add_genre
)
from tests.select_content import (
    select_movie,
    select_series,
    select_episode,
    select_genre
)
from tests.update_content import (
    update_movie,
    update_series,
    update_episode,
    update_genre
)
from tests.delete_content import (
    delete_movie,
    delete_series,
    delete_episode,
    delete_genre
)


# ADD CONTENT
def test_add_movie():
    assert add_movie() == 201
    
def test_add_series():
    assert add_series() == 201
    
def test_add_episode():
    assert add_episode() == 201
    
def test_add_genre():
    assert add_genre() == 201
    
    
# SELECT CONTENT
def test_select_movie():
    assert select_movie() == 200
    
def test_select_series():
    assert select_series() == 200
    
def test_select_episode():
    assert select_episode() == 200
    
def test_select_genre():
    assert select_genre() == 200
    
    
# UPDATE CONTENT
def test_update_movie():
    assert update_movie() == 200
    
def test_update_series():
    assert update_series() == 200
    
def test_update_episode():
    assert update_episode() == 200
    
def test_update_genre():
    assert update_genre() == 200
    

# DELETE CONTENT
def test_delete_movie():
    assert delete_movie() == 200
    
def test_delete_series():
    assert delete_series() == 200
    
def test_delete_episode():
    assert delete_episode() == 200
    
def test_delete_genre():
    assert delete_genre() == 200