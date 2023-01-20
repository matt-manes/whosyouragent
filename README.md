# whosyouragent
Self updating package for generating random user agent strings.<br>
Install with:
<pre>pip install whosyouragent</pre>
New browser versions will be checked for when the module is imported if it's been a week or more since the last update.<br>
Usage:
<pre>
from whosyouragent import get_agent
print(get_agent())
</pre>
produces:
<pre>
Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.98 Safari/537.36 Vivaldi/5.6
</pre>

