using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class C_node 
{
    public Node nd;
    public C_node next;
    
    public C_node(Node d)
    {
        nd = d;
        this.next = null;
    }
}