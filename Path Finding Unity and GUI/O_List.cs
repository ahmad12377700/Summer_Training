using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using static UnityEditor.PlayerSettings;

 public class O_List 
{
    public O_node head ;
    public O_node tail ;
    
    public O_List()
    {
        head = null;
        tail = null;
    }

    public O_node Add_node(Node nod)
    {
        O_node n = null;
        if (nod != null)
        {
            n = new O_node(null, nod, null);
            if (head == null)
            {
                head = n;
                tail = n;
            }
            else
            {
                n.prev = tail;
                tail.next = n;
                tail = n;
            }
        }
        return n;
    }
   
    public void Remove_node(O_node nod)
    {
        if (nod == head) 
        { 
            head = nod.next; 
            if (head !=null)
                head.prev = null;
            else 
                tail = null;
            return;
        }
        
        if (nod == tail) 
        {  
            tail = nod.prev;
            nod.prev = null;
            if (tail != null)
                tail.next = null;
            else 
                head = null;
            return;
        }
        
        nod.prev.next = nod.next;
        nod.next.prev = nod.prev;
        nod.prev = null;
        nod.next = null;
    }
    
    public O_node Lowest_cost()
    {
        O_node p = head;
        O_node minCost_nd = null;
        float t_cost = 100000.0f;
        while (p != null)
        {
            if (p.nd.total_cost < t_cost)
            {
                minCost_nd = p;
                t_cost = p.nd.total_cost; 
            }
            p = p.next;
        }
        return minCost_nd;
    }

    public bool Node_found(Node n)
    {
        O_node nod = head;
        bool found = false;
        while (nod != null)
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
    
    public void Display_list()
    {
        O_node p = head;
        while (p != null)
        {
            Debug.Log(p.nd.name + "\t" + p.nd.total_cost + "\n");
            p = p.next;
        }

    }
}