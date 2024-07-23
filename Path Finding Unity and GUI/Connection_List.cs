using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Connection_List 
{
    public Link head = null;
    public Link tail = null;

    public Connection_List(Link l)
    {
        head = l;
        tail = l;
    }
    
    public void Inser_Link(Link l)
    {
        if (head == null)
        {
            head = l;
            tail = l;
            return;
        }
        else
        {
            tail.next_Lnk = l;
            tail = l;
        }

    }
}
