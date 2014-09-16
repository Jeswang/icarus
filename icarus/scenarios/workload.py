"""Functions for generating traffic workloads 
"""
import random
from icarus.tools import TruncatedZipfDist


__all__ = [
    'uniform_req_gen',
    'globetraff_req_gen',
    'custom_req_gendef'
]


def uniform_req_gen(topology, n_contents, alpha, rate=12.0,
                    n_warmup=10 ** 5, n_measured=4 * 10 ** 5, seed=None):
    """This function generates events on the fly, i.e. instead of creating an 
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.
    
    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower.
    
    These requests are Poisson-distributed while content popularity is
    Zipf-distributed
    
    Parameters
    ----------
    topology : fnss.Topology
        The topology to which the workload refers
    n_contents : int
        The number of content object
    alpha : float
        The Zipf alpha parameter
    rate : float
        The mean rate of requests per second
    n_warmup : int
        The number of warmup requests (i.e. requests executed to fill cache but
        not logged)
    n_measured : int
        The number of logged requests after the warmup
    
    Returns
    -------
    events : iterator
        Iterator of events. Each event is a 2-tuple where the first element is
        the timestamp at which the event occurs and the second element is a
        dictionary of event attributes.
    """
    receivers = [v for v in topology.nodes_iter()
                 if topology.node[v]['stack'][0] == 'receiver']
    zipf = TruncatedZipfDist(alpha, n_contents)
    random.seed(seed)

    req_counter = 0
    t_event = 0.0
    while req_counter < n_warmup + n_measured:
        t_event += (random.expovariate(rate))
        receiver = random.choice(receivers)
        content = int(zipf.rv())
        log = (req_counter >= n_warmup)
        event = {'receiver': receiver, 'content': content, 'log': log}
        yield (t_event, event)
        req_counter += 1
    raise StopIteration()


def globetraff_req_gen(topology, content_file, request_file):
    """Parse requests from GlobeTraff workload generator
    
    Parameters
    ----------
    topology : fnss.Topology
        The topology to which the workload refers
    content_file : str
        The GlobeTraff content file
    request_file : str
        The GlobeTraff request file
    """
    raise NotImplementedError('Not yet implemented')


def custom_req_gendef(topology, n_contents, alpha, rate=12.0,
                      n_warmup=10 ** 5, n_measured=4 * 10 ** 5, seed=None):
    """This function generates events on the fly, i.e. instead of creating an 
    event schedule to be kept in memory, returns an iterator that generates
    events when needed.
    
    This is useful for running large schedules of events where RAM is limited
    as its memory impact is considerably lower.
    
    These requests are Poisson-distributed while content popularity is
    Zipf-distributed
    
    Parameters
    ----------
    topology : fnss.Topology
        The topology to which the workload refers
    n_contents : int
        The number of content object
    alpha : float
        The Zipf alpha parameter
    rate : float
        The mean rate of requests per second
    n_warmup : int
        The number of warmup requests (i.e. requests executed to fill cache but
        not logged)
    n_measured : int
        The number of logged requests after the warmup
    
    Returns
    -------
    events : iterator
        Iterator of events. Each event is a 2-tuple where the first element is
        the timestamp at which the event occurs and the second element is a
        dictionary of event attributes.
    """
    receivers = [v for v in topology.nodes_iter()
                 if topology.node[v]['stack'][0] == 'cache']

    sub_request = [3, 1, 4, 4, 1, 3, 4, 4, 4, 3, 2, 1, 1, 3, 4, 2, 1, 1, 2, 1, 2, 1, 3, 4, 4, 3, 1, 3, 4, 2, 2, 3, 2, 2,
                   3, 3, 4, 4, 3, 2]

    zipfs = []
    zipfs.append(TruncatedZipfDist(alpha, n_contents * 0.2))
    zipfs.append(TruncatedZipfDist(alpha, n_contents * 0.2))
    zipfs.append(TruncatedZipfDist(alpha, n_contents * 0.2))
    zipfs.append(TruncatedZipfDist(alpha, n_contents * 0.2))
    zipfs.append(TruncatedZipfDist(alpha, n_contents * 0.2))

    random.seed(seed)

    req_counter = 0
    t_event = 0.0
    while req_counter < n_warmup + n_measured:
        t_event += (random.expovariate(rate))
        receiver = random.choice(receivers)
        if random.random() > 0.8:
            zipf = zipfs[0]
            content_begin = 0
        else:
            category = sub_request[receiver]
            zipf = zipfs[category]
            content_begin = n_contents * (0.2 + (category-1)*0.2)

        content = content_begin + int(zipf.rv())
        log = (req_counter >= n_warmup)
        event = {'receiver': receiver, 'content': int(content), 'log': log}
        yield (t_event, event)
        req_counter += 1
    raise StopIteration()
