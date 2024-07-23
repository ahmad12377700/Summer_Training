using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class C_List 
{
    public C_node head;
    public C_node tail;
    
    public C_List()
    {
        head = null;
        tail = null;
    }

    public void Add_node(Node n)
    {
        C_node d = new C_node(n);
        if (head == null)
        {            
            head = d;
            tail = d;
        }
        else
        {           
            tail.next = d;
            tail = d;
        }  
    }
    
    public bool Node_found(Node n)
    {
        C_node nod=head;
        bool found= false;
        while (nod!=null)
        {
            if (nod.nd == n)
            {
                found = true;
                break;
            }  
            nod = nod.next;
        }
        return found;
    }
    
    public void optimize_path(Player_Loc loc)
    {
        if (head != null && head.next != null) 
        {
            Player_Loc loc1 = new Player_Loc(head.nd.x, head.nd.z);
            float d1 = loc.getDist(head.nd);
            float d2 = loc1.getDist(head.next.nd);
            float d3 = loc.getDist(head.next.nd);
            
            if (d3 < (d1 + d2))
            {
                head = head.next;
            }
        }
    }

}