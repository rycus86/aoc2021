from shared.utils import *

from collections import namedtuple


Coordinate3D = namedtuple('Coordinate3D', ('x', 'y', 'z'))


class Day24(Solution):
    positions: List[Coordinate3D]
    velocities: List[Coordinate3D]

    max_steps = 10**2

    def setup(self):
        self.positions = list()
        self.velocities = list()

        for line in self.input_lines():
            position, velocity = map(str.strip, line.split('@'))
            px, py, pz = map(int, map(str.strip, position.split(',')))
            vx, vy, vz = map(int, map(str.strip, velocity.split(',')))
            self.positions.append(Coordinate3D(px, py, pz))
            self.velocities.append(Coordinate3D(vx, vy, vz))

    def part_1(self):
        min_pos = 200000000000000
        max_pos = 400000000000000

        for idx1 in range(len(self.positions) - 1):
            for idx2 in range(idx1 + 1, len(self.positions)):
                ix, iy = self.find_intersection_2d(idx1, idx2)
                if ix is None:
                    continue  # parallel

                p1, v1 = self.positions[idx1], self.velocities[idx1]
                p2, v2 = self.positions[idx2], self.velocities[idx2]
                if p1.x < ix and v1.x < 0 or p1.x > ix and v1.x > 0 or p2.x < ix and v2.x < 0 or p2.x > ix and v2.x > 0:
                    continue  # these met in the past

                if min_pos <= ix <= max_pos and min_pos <= iy <= max_pos:
                    self.add_result()  # ok, within bounds

    def find_intersection_2d(self, idx1, idx2):
        p1, v1 = self.positions[idx1], self.velocities[idx1]
        p2, v2 = self.positions[idx2], self.velocities[idx2]

        return self.find_intersection_2d_of_pv(p1, v1, p2, v2)

    def find_intersection_2d_of_pv(self, p1, v1, p2, v2):
        x1, y1 = p1.x, p1.y
        x2, y2 = x1 + v1.x, y1 + v1.y
        x3, y3 = p2.x, p2.y
        x4, y4 = x3 + v2.x, y3 + v2.y

        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
        d = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if not d:
            return None, None

        rx = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / d
        ry = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / d
        return rx, ry

    def part_2(self):
        return self.solve_using_scipy()

        # note: this ended up being too slow

        # p1, v1 = self.positions[0], self.velocities[0]
        # p2, v2 = None, None
        # p3, v3 = None, None
        #
        # for idx in range(1, len(self.positions)):
        #     ix, iy = self.find_intersection_2d(0, idx)
        #     if ix is not None:
        #         if p2 is None:
        #             p2, v2 = self.positions[idx], self.velocities[idx]
        #         else:
        #             p3, v3 = self.positions[idx], self.velocities[idx]
        #             break
        #
        # for rp, rv in self.iter_candidates(p1, v1, p2, v2):
        #     if self.check_candidate(rp, rv, p3, v3):
        #         if self.check_all_candidates(rp, rv):
        #             return rp.x + rp.y + rp.z

    def solve_using_scipy(self):
        from scipy.optimize import fsolve

        # based on https://github.com/mrphlip/aoc/blob/master/2023/24.md
        def equations(pv):
            x1, y1, z1, vx1, vy1, vz1 = pv
            eq = []
            for idx in range(2, 5):
                pi, vi = self.positions[idx], self.velocities[idx]
                eq.append((x1-pi.x)*(vy1-vi.y) - (y1-pi.y)*(vx1-vi.x))
                eq.append((x1-pi.x)*(vz1-vi.z) - (z1-pi.z)*(vx1-vi.x))
            return eq

        x, y, z, *_ = fsolve(equations, (*self.positions[0], *self.velocities[0]))
        return round(x + y + z)

    def iter_candidates(self, p1, v1, p2, v2):
        for t1 in range(self.max_steps):
            if (p1.x + v1.x * t1) % v2.x != p2.x % v2.x:
                continue
            elif (p1.y + v1.y * t1) % v2.y != p2.y % v2.y:
                continue
            elif (p1.z + v1.z * t1) % v2.z != p2.z % v2.z:
                continue

            for t2 in range(self.max_steps):
                candidate = self.find_candidate(p1, v1, t1, p2, v2, t2)
                if candidate:
                    rp, rv = candidate
                    yield rp, rv

    def find_candidate(self, p1, v1, t1, p2, v2, t2):
        x1, y1, z1 = p1.x + v1.x * t1, p1.y + v1.y * t1, p1.z + v1.z * t1
        x2, y2, z2 = p2.x + v2.x * t2, p2.y + v2.y * t2, p2.z + v2.z * t2

        dx, dy, dz, dt = x2 - x1, y2 - y1, z2 - z1, t2 - t1
        if dt == 0:
            if dx != 0 or dy != 0 or dz != 0:
                return
        elif dx % dt != 0:
            return
        elif dy % dt != 0:
            return
        elif dz % dt != 0:
            return

        rv = Coordinate3D(dx // dt, dy // dt, dz // dt)
        rp = Coordinate3D(x1 - t1 * rv.x, y1 - t1 * rv.y, z1 - t1 * rv.z)

        return rp, rv

    def check_candidate(self, p1, v1, p2, v2):
        ip, iv = self.find_intersection_2d_of_pv(p1, v1, p2, v2)
        if ip is None:
            return False

        for t1 in range(self.max_steps):
            if (p1.x + v1.x * t1) % v2.x != p2.x % v2.x:
                continue

            for t2 in range(self.max_steps):
                if p1.x + v1.x * t1 != p2.x + v2.x * t2:
                    continue
                elif p1.y + v1.y * t1 != p2.y + v2.y * t2:
                    continue
                elif p1.z + v1.z * t1 != p2.z + v2.z * t2:
                    continue
                else:
                    return True

    def check_all_candidates(self, rp, rv):
        for idx in range(len(self.positions)):
            p2, v2 = self.positions[idx], self.velocities[idx]
            if not self.check_candidate(rp, rv, p2, v2):
                return False

        return True


Day24(__file__).solve()
