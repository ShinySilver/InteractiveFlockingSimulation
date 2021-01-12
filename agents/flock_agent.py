from agents.agent import Agent
import numpy as np

from agents.green_lighthouse import GreenLighthouse
from agents.red_lighthouse import RedLighthouse

class FlockAgent(Agent):
    def __init__(self,
                 context,
                 avoidance_distance: float = 20.0,
                 alignment_strength: float = 0.5,
                 cohesion_strength: float = 0.3,
                 avoidance_strength: float = 0.2,
                 pos=(0, 0),
                 speed: float = 10.0,
                 rotation: float = 0.0,
                 rotation_speed: float = 2.0,
                 focus: float = 50.0,
                 nimbus: float = 100.0,
                 is_debug: bool = False):
        """
        Parameters
        ----------
        avoidance_distance is the minimum distance before triggering avoidance mechanism override
        alignment_strength is the alignment behaviour modifier
        cohesion_strength is the cohesion behaviour modifier
        avoidance_strength is the avoidance behaviour modifier
        speed is the distance increment per tick
        rotation_speed is the rotation increment per tick
        pos @optional is the (x, y) initial position
        focus @optional is the can-see distance modifier
        nimbus @optional is the can-be-seen distance modifier
        isDebug @optional whether or not this agent is used for debugging
        """
        super().__init__(context, pos, focus, nimbus)
        self.avoidance_distance = avoidance_distance
        self.alignment_strength = alignment_strength
        self.cohesion_strength = cohesion_strength
        self.avoidance_strength = avoidance_strength
        self.speed = speed
        self.rotation = rotation
        self.rotation_speed = rotation_speed

        # TODO: Add modifier balancing / normalization

        self.direction = np.array((np.cos(self.rotation), np.sin(self.rotation)))

        self.id = None
        self.is_debug = is_debug

    def prepare_update(self):
        super().prepare_update()

        avoidance = [0, 0, 0]  # x, y, count
        alignment = [0, 0, 0]
        cohesion = [0, 0, 0]
        lighthouse = [0, 0, 0]
        distance, relpos = 0.0, 0.0

        # Flock behaviour handling
        for agent in self.context.get_agents(FlockAgent):

            # Ignore self
            if agent is self:
                continue

            # Computing distance to target, and the unit vector going from self to target
            distance = self.distance_to(agent)
            if self.in_nimbus_of(agent, cached_distance=distance):
                agent_weight = (self.focus-distance)**2

                if distance != 0:
                    relpos = self._shortest(agent.pos - self.pos, 0, self.context.width)/ distance
                else:
                    relpos = (0,0)

                # Handling alignment
                if self.can_focus(agent, distance):
                    alignment[0] = alignment[0] + np.cos(agent.rotation)*agent_weight
                    alignment[1] = alignment[1] + np.sin(agent.rotation)*agent_weight
                    alignment[2] += agent_weight

                if distance <= self.avoidance_distance:
                    # Handling avoidance
                    agent_weight = (self.avoidance_distance - distance) ** 2
                    avoidance[0] = avoidance[0] - relpos[0] * agent_weight
                    avoidance[1] = avoidance[1] - relpos[1] * agent_weight
                    avoidance[2] += agent_weight
                else:
                    # Handling cohesion
                    cohesion[0] = cohesion[0] + relpos[0]*agent_weight
                    cohesion[1] = cohesion[1] + relpos[1]*agent_weight
                    cohesion[2] += agent_weight

        if abs(avoidance[2] + alignment[2] + cohesion[2]) > 1e-2:
            tmp = (avoidance, alignment, cohesion)
            tmp2 = (self.avoidance_strength, self.alignment_strength, self.cohesion_strength)
            self.direction = [np.sum([tmp[j][i] / tmp[j][2] * tmp2[j] for j in range(3) if tmp[j][2] > 0]) for i in
                                   range(2)]
            self.direction = self.direction/np.linalg.norm(self.direction)

        # Lighthouse behaviour
        target_angles = []

        for agent in self.context.get_agents(GreenLighthouse):
            distance = self.distance_to(agent)
            if self.in_nimbus_of(agent, cached_distance=distance):
                if distance != 0:
                    relpos = self._shortest(agent.pos - self.pos, 0, self.context.width) / distance
                else:
                    relpos = (0,0)


                signed_angle = np.arctan2(*relpos[::-1]) - np.arctan2(*self.direction[::-1])
                signed_angle = signed_angle%(2*np.pi)
                if signed_angle > np.pi:
                    signed_angle-=2*np.pi
                alignment_weight = (np.pi-signed_angle)/np.pi
                distance_weight = (distance/agent.nimbus)
                weight = alignment_weight*distance_weight
                target_angle = np.arctan(self.direction[1] / self.direction[0])

                if(signed_angle>=0 and abs(signed_angle)<np.pi/2):
                    target_angle += (signed_angle-np.sign(signed_angle)*np.pi/2*(distance-self.nimbus)/self.nimbus)*weight

                target_angles.append(target_angle)

        for agent in self.context.get_agents(RedLighthouse):
            distance = self.distance_to(agent)
            if self.in_nimbus_of(agent, cached_distance=distance):
                if distance != 0:
                    relpos = self._shortest(agent.pos - self.pos, 0, self.context.width) / distance
                else:
                    relpos = (0,0)


                signed_angle = np.arctan2(*relpos[::-1]) - np.arctan2(*self.direction[::-1])
                signed_angle = signed_angle%(2*np.pi)
                if signed_angle > np.pi:
                    signed_angle-=2*np.pi
                alignment_weight = (np.pi-signed_angle)/np.pi
                distance_weight = (distance/agent.nimbus)
                weight = alignment_weight*distance_weight
                target_angle = np.arctan(self.direction[1] / self.direction[0])

                if(signed_angle<=0 and abs(signed_angle)<np.pi/2):
                    target_angle += (signed_angle-np.sign(signed_angle)*np.pi/2*(distance-self.nimbus)/self.nimbus)*weight

                target_angles.append(target_angle)

        if(target_angles != []):
            target_angle = np.mean(target_angles)
            self.direction = (np.cos(target_angle), np.sin(target_angle))



    def apply_update(self):
        target_angle = np.arctan(self.direction[1]/self.direction[0])
        if self.direction[0]<0:
            target_angle -=np.pi

        relative_oriented_angle = (target_angle-self.rotation)%(2*np.pi)
        if relative_oriented_angle>np.pi:
            relative_oriented_angle-=2*np.pi
        if(abs(relative_oriented_angle)<self.rotation_speed):
            self.rotation = target_angle
        elif relative_oriented_angle>0:
            self.rotation += self.rotation_speed
        elif relative_oriented_angle<0:
            self.rotation -= self.rotation_speed

        delta = (np.cos(self.rotation) * self.speed, np.sin(self.rotation) * self.speed)
        self.pos = self.pos + delta


    def render(self, client):
        if self.id is None:
            self.id = client.create_oval(self.pos[0] - 5, self.pos[1] - 5, self.pos[0] + 5, self.pos[1] + 5, fill="blue",
                               outline="white")
            return
        client.coords(self.id, self.pos[0] - 5, self.pos[1] - 5, self.pos[0] + 5, self.pos[1] + 5)
