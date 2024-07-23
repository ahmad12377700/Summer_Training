using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Link 
{
    public Node t_node;
    public float l_cost;
    public Link next_Lnk = null;

    public Link(Node nd, float cost)
    {
        t_node = nd;
        l_cost = cost;
        next_Lnk = null;
    }

}
