import smach

class Square(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['low_battery'])

    def execute(self, data):
        if(True==True):
            return "good"
        else:
            return "bad"


class ReturnToLand(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'])

    def execute(self, data):
        if(True==True):
            return "good"
        else:
            return "bad"


class Takeoff(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['good', 'error'])


state_machine = smach.StateMachine(outcomes=['good','bad'], )


def main():
    while True:
        with state_machine:
            smach.StateMachine.add("TAKEOFF", Takeoff(), transitions={"good":"SQUARE", "error":"RTL"})
            smach.StateMachine.add("RTL", ReturnToLand(), transitions={"success":"DISARM", "error":"DISARM"})
            smach.StateMachine.add("SQUARE", Square(), transitions={"low_battery":"RTL"})

        output = state_machine.execute()
        print output



if __name__ == "__main__":
    main()
