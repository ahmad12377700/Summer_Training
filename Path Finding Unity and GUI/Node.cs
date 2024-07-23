using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Node 
{
    public Connection_List c_l;
    public float total_cost;
    public Node parent;
    public float x;
    public float z;
    public string name;
    public Node next;
  
    public Node(string nam, float xx, float zz)
    {
        c_l = null;
        total_cost = 0;
        parent = null;
        x = xx;
        z = zz;
        name = nam;
        next = null;
    }

    public void Add_Fanout( O_List o_lst, C_List c_lst)
    {
        Link l;
        if (c_l != null)
        {
            l = c_l.head;
            while (l != null)
            {
                if (!(c_lst.Node_found(l.t_node)))
                {
                    if (!(o_lst.Node_found(l.t_node))) { 
                        o_lst.Add_node(l.t_node);
                        l.t_node.total_cost = l.l_cost + this.total_cost;
                        l.t_node.parent = this;
                        Debug.Log(l.t_node.name + " has Father " + this.name);
                    }
                    else{
                        if (l.t_node.total_cost > this.total_cost+l.l_cost)
                        {
                            l.t_node.total_cost = l.l_cost + this.total_cost;
                            l.t_node.parent = this;
                        }
                    }
                }
                l = l.next_Lnk;
            }
        }
    }

}
