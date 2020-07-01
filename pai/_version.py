from __future__ import absolute_import

version_info = (0, 1, 0)

_num_index = max(idx if isinstance(v, int) else 0
                 for idx, v in enumerate(version_info))
__version__ = '.'.join(map(str, version_info[:_num_index + 1])) + \
              ''.join(version_info[_num_index + 1:])
