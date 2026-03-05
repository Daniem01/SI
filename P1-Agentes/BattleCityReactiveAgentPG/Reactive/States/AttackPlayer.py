from StateMachine.State import State
from States.AgentConsts import AgentConsts


class AttackPlayer(State):

    def __init__(self, id):
        super().__init__(id)
        self.obstaculos = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.OTHER,
        ]

    def Update(self, perception, map, agent):
        # Primero debemos mirar en que direccion debe ir el tanque
        # en funcion de donde esta el enemigo para "apuntar"

        # Si el agente y el jugador estan en la misma columna
        if perception[AgentConsts.AGENT_X] == perception[AgentConsts.PLAYER_X]:
            if perception[AgentConsts.AGENT_Y] < perception[AgentConsts.PLAYER_Y]:
                # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                if (
                    perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] > 1
                ):
                    return AgentConsts.MOVE_DOWN, False
                # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                elif (
                    perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_RIGHT]
                            in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                        ):
                            return AgentConsts.MOVE_UP, False
                        else:
                            return AgentConsts.MOVE_RIGHT, False
                    else:
                        return AgentConsts.MOVE_LEFT, False
                else:
                    return AgentConsts.MOVE_DOWN, True
            else:
                # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                if (
                    perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] > 1
                ):
                    return AgentConsts.MOVE_UP, False
                # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                elif (
                    perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                ):
                    # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_RIGHT]
                            in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                        ):
                            return AgentConsts.MOVE_DOWN, False
                        else:
                            return AgentConsts.MOVE_RIGHT, False
                    else:
                        return AgentConsts.MOVE_LEFT, False
                else:
                    return AgentConsts.MOVE_UP, True

        # Si el agente y el jugador estan en la misma fila
        elif perception[AgentConsts.AGENT_Y] == perception[AgentConsts.PLAYER_Y]:
            if perception[AgentConsts.AGENT_X] < perception[AgentConsts.PLAYER_X]:
                # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                if (
                    perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] > 1
                ):
                    return AgentConsts.MOVE_RIGHT, False
                # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                elif (
                    perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                        ):
                            return AgentConsts.MOVE_LEFT, False
                        else:
                            return AgentConsts.MOVE_UP, False
                    else:
                        return AgentConsts.MOVE_DOWN, False
                else:
                    return AgentConsts.MOVE_RIGHT, True
            else:
                # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                if (
                    perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] > 1
                ):
                    return AgentConsts.MOVE_LEFT, False
                # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                elif (
                    perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                        ):
                            return AgentConsts.MOVE_RIGHT, False
                        else:
                            return AgentConsts.MOVE_UP, False
                    else:
                        return AgentConsts.MOVE_DOWN, False
                else:
                    return AgentConsts.MOVE_LEFT, True

        # Si no estan alineados pero esta cerca querremos que intente alinearse con el jugador
        # para poder intentar destruirlo
        else:
            # Si el jugador es mas facil alinearlo en el eje x
            if abs(
                perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]
            ) > abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y]):
                if perception[AgentConsts.AGENT_Y] < perception[AgentConsts.PLAYER_Y]:
                    # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] > 1
                    ):
                        return AgentConsts.MOVE_DOWN, False
                    # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                    elif (
                        perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                        ):
                            if (
                                perception[AgentConsts.NEIGHBORHOOD_RIGHT]
                                in self.obstaculos
                                and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                            ):
                                return AgentConsts.MOVE_UP, False
                            else:
                                return AgentConsts.MOVE_RIGHT, False
                        else:
                            return AgentConsts.MOVE_LEFT, False
                    else:
                        return AgentConsts.MOVE_DOWN, True
                else:
                    # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] > 1
                    ):
                        return AgentConsts.MOVE_UP, False
                    # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                    elif (
                        perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                    ):
                        # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                        ):
                            if (
                                perception[AgentConsts.NEIGHBORHOOD_RIGHT]
                                in self.obstaculos
                                and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                            ):
                                return AgentConsts.MOVE_DOWN, False
                            else:
                                return AgentConsts.MOVE_RIGHT, False
                        else:
                            return AgentConsts.MOVE_LEFT, False
                    else:
                        return AgentConsts.MOVE_UP, True
            # Si es mas facil y por el eje x
            else:
                if perception[AgentConsts.AGENT_X] < perception[AgentConsts.PLAYER_X]:
                    # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] > 1
                    ):
                        return AgentConsts.MOVE_RIGHT, False
                    # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                    elif (
                        perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                        ):
                            if (
                                perception[AgentConsts.NEIGHBORHOOD_UP]
                                in self.obstaculos
                                and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                            ):
                                return AgentConsts.MOVE_LEFT, False
                            else:
                                return AgentConsts.MOVE_UP, False
                        else:
                            return AgentConsts.MOVE_DOWN, False
                    else:
                        return AgentConsts.MOVE_RIGHT, True
                else:
                    # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] > 1
                    ):
                        return AgentConsts.MOVE_LEFT, False
                    # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                    elif (
                        perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                        ):
                            if (
                                perception[AgentConsts.NEIGHBORHOOD_UP]
                                in self.obstaculos
                                and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                            ):
                                return AgentConsts.MOVE_RIGHT, False
                            else:
                                return AgentConsts.MOVE_UP, False
                        else:
                            return AgentConsts.MOVE_DOWN, False
                    else:
                        return AgentConsts.MOVE_LEFT, True

    def PocesaMovimiento(self, intencionMov, perception):
        if intencionMov == AgentConsts.MOVE_DOWN:
            if (
                perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] > 1
            ):
                return AgentConsts.MOVE_DOWN, False
            # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
            elif (
                perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
            ):
                if (
                    perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                    ):
                        return AgentConsts.MOVE_UP, False
                    else:
                        return AgentConsts.MOVE_RIGHT, False
                else:
                    return AgentConsts.MOVE_LEFT, False
            else:
                return AgentConsts.MOVE_DOWN, True

        elif intencionMov == AgentConsts.MOVE_UP:
            if (
                perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] > 1
            ):
                return AgentConsts.MOVE_UP, False
            # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
            elif (
                perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
            ):
                # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                if (
                    perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                    ):
                        return AgentConsts.MOVE_DOWN, False
                    else:
                        return AgentConsts.MOVE_RIGHT, False
                else:
                    return AgentConsts.MOVE_LEFT, False
            else:
                return AgentConsts.MOVE_UP, True

        elif intencionMov == AgentConsts.MOVE_RIGHT:
            if perception[AgentConsts.AGENT_X] < perception[AgentConsts.PLAYER_X]:
                # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
                if (
                    perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] > 1
                ):
                    return AgentConsts.MOVE_RIGHT, False
                # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
                elif (
                    perception[AgentConsts.NEIGHBORHOOD_RIGHT] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                    ):
                        if (
                            perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                            and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                        ):
                            return AgentConsts.MOVE_LEFT, False
                        else:
                            return AgentConsts.MOVE_UP, False
                    else:
                        return AgentConsts.MOVE_DOWN, False
                else:
                    return AgentConsts.MOVE_RIGHT, True

        else:
            # Si lo que hay en esa direccion es un muro indestructible avanzamos pero no disparamos
            if (
                perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] > 1
            ):
                return AgentConsts.MOVE_LEFT, False
            # Si tenemos un muro indestructible o un rio al lado no iremos hacia alla
            elif (
                perception[AgentConsts.NEIGHBORHOOD_LEFT] in self.obstaculos
                and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= 1
            ):
                if (
                    perception[AgentConsts.NEIGHBORHOOD_DOWN] in self.obstaculos
                    and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= 1
                ):
                    if (
                        perception[AgentConsts.NEIGHBORHOOD_UP] in self.obstaculos
                        and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= 1
                    ):
                        return AgentConsts.MOVE_RIGHT, False
                    else:
                        return AgentConsts.MOVE_UP, False
                else:
                    return AgentConsts.MOVE_DOWN, False
            else:
                return AgentConsts.MOVE_LEFT, True
