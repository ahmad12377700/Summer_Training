using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class O_node
{
    public O_node prev;
    public Node nd;
    public O_node next;
    
    public O_node(O_node p, Node n, O_node nx) 
    {
        prev = p;
        nd = n;
        next = nx;
    }
}
